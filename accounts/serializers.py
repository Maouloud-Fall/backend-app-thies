from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Sérialiseur pour afficher les informations des utilisateurs."""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone', 'birth_date']
        read_only_fields = ['id', 'role']

    def validate_username(self, value):
        """Validation pour garantir que username contient un prénom et un nom avec espaces autorisés."""
        if len(value.split()) < 2:
            raise serializers.ValidationError("Le nom d'utilisateur doit contenir un prénom et un nom.")

        if not value.replace(" ", "").isalnum():  # Permettre les espaces mais pas les caractères spéciaux
            raise serializers.ValidationError("Le nom d'utilisateur ne doit contenir que des lettres et des espaces.")

        return value

class RegisterSerializer(serializers.ModelSerializer):
    """Sérialiseur pour l'enregistrement des nouveaux utilisateurs."""

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True, required=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'phone', 'birth_date']

    def validate(self, attrs):
        """Validation des mots de passe et du username."""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})

        # Vérifier que username contient un prénom et un nom avec espaces autorisés
        if len(attrs['username'].split()) < 2:
            raise serializers.ValidationError({"username": "Le nom d'utilisateur doit contenir un prénom et un nom."})

        if not attrs['username'].replace(" ", "").isalnum():
            raise serializers.ValidationError({"username": "Le nom d'utilisateur ne doit contenir que des lettres et des espaces."})

        return attrs

    def create(self, validated_data):
        """Création d'un nouvel utilisateur avec un mot de passe sécurisé."""
        validated_data.pop('password2')  # Supprimer password2 qui n'est pas nécessaire pour l'enregistrement
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user