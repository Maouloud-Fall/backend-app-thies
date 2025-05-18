from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Sérialiseur complet pour les utilisateurs avec statut en ligne."""

    is_online = serializers.SerializerMethodField(read_only=True)
    last_activity = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'role',
            'phone', 'birth_date', 'full_name',
            'is_online', 'last_activity'
        ]
        read_only_fields = ['id', 'role', 'is_online', 'last_activity']

    def get_is_online(self, obj):
        """Détermine si l'utilisateur est en ligne."""
        return obj.is_online

    def validate_username(self, value):
        """
        Validation du username :
        - Doit contenir prénom et nom
        - Ne contient que des caractères alphanumériques et espaces
        """
        value = value.strip()

        if len(value.split()) < 2:
            raise serializers.ValidationError(
                "Le nom d'utilisateur doit contenir un prénom et un nom séparés par un espace."
            )

        if not all(part.isalnum() for part in value.split()):
            raise serializers.ValidationError(
                "Seuls les caractères alphanumériques et espaces sont autorisés."
            )

        return value


class RegisterSerializer(serializers.ModelSerializer):
    """Sérialiseur pour l'inscription des utilisateurs avec validation renforcée."""

    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password',
            'password2', 'phone', 'birth_date', 'full_name'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'full_name': {'required': True}
        }

    def validate(self, data):
        """Validation globale des données d'inscription."""
        # Validation des mots de passe
        if data['password'] != data['password2']:
            raise serializers.ValidationError({
                'password': 'Les mots de passe ne correspondent pas.'
            })

        # Validation du username
        username = data.get('username', '')
        if len(username.split()) < 2:
            raise serializers.ValidationError({
                'username': 'Veuillez entrer votre prénom et nom complet.'
            })

        # Validation de l'email unique
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({
                'email': 'Un utilisateur avec cet email existe déjà.'
            })

        return data

    def create(self, validated_data):
        """Crée un nouvel utilisateur avec mot de passe haché."""
        validated_data.pop('password2')
        try:
            user = User.objects.create_user(**validated_data)
            return user
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict)


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """Sérialiseur pour la mise à jour sécurisée du profil."""

    current_password = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = [
            'full_name', 'email', 'phone', 'birth_date',
            'current_password', 'new_password', 'confirm_password'
        ]
        extra_kwargs = {
            'email': {'required': False},
            'phone': {'required': False},
            'birth_date': {'required': False}
        }

    def validate(self, data):
        """Validation pour le changement de mot de passe."""
        password_fields = [
            data.get('current_password'),
            data.get('new_password'),
            data.get('confirm_password')
        ]

        # Si un champ mot de passe est rempli, tous doivent l'être
        if any(password_fields) and not all(password_fields):
            raise serializers.ValidationError(
                "Tous les champs de mot de passe sont requis pour une modification."
            )

        # Vérification de la correspondance des nouveaux mots de passe
        if password_fields[1] and password_fields[1] != password_fields[2]:
            raise serializers.ValidationError({
                'new_password': 'Les nouveaux mots de passe ne correspondent pas.'
            })

        # Vérification du mot de passe actuel
        if password_fields[0] and not self.instance.check_password(password_fields[0]):
            raise serializers.ValidationError({
                'current_password': 'Le mot de passe actuel est incorrect.'
            })

        return data

    def update(self, instance, validated_data):
        """Mise à jour sécurisée du profil."""
        # Mise à jour des champs de base
        for field in ['full_name', 'email', 'phone', 'birth_date']:
            if field in validated_data:
                setattr(instance, field, validated_data[field])

        # Mise à jour du mot de passe si fourni
        if validated_data.get('new_password'):
            instance.set_password(validated_data['new_password'])

        instance.save()
        return instance