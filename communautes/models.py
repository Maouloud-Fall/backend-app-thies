from django.db import models
from django.core.validators import EmailValidator, RegexValidator
from django.conf import settings
from django.utils import timezone


class Communaute(models.Model):
    DOMAINE_CHOICES = [
        ('PROG', 'Programmation'),
        ('MARK', 'Marketing'),
        ('COMPT', 'Comptabilité'),
        ('DESIGN', 'Design'),
        ('RH', 'Ressources Humaines'),
        ('AUTRE', 'Autre'),
    ]

    # Champs existants
    nom_entreprise = models.CharField(
        max_length=100,
        verbose_name="Nom de l'entreprise"
    )

    adresse = models.TextField(verbose_name="Adresse")

    telephone = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^\+?[0-9 ]+$', 'Numéro de téléphone invalide')],
        verbose_name="Téléphone"
    )

    email = models.EmailField(
        validators=[EmailValidator()],
        verbose_name="Email"
    )

    domaine = models.CharField(
        max_length=10,
        choices=DOMAINE_CHOICES,
        verbose_name="Domaine d'activité"
    )

    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )

    site_web = models.URLField(
        blank=True,
        null=True,
        verbose_name="Site web"
    )

    # Nouveaux champs pour la gestion des permissions
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='communautes_crees',
        verbose_name="Créé par"
    )

    last_modified = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière modification"
    )

    is_public = models.BooleanField(
        default=True,
        verbose_name="Visible publiquement"
    )

    class Meta:
        verbose_name = "Membre de la communauté"
        verbose_name_plural = "Membres de la communauté"
        ordering = ['nom_entreprise']
        indexes = [
            models.Index(fields=['nom_entreprise']),
            models.Index(fields=['domaine']),
            models.Index(fields=['is_public']),
        ]
        permissions = [
            ("can_approve_communaute", "Peut approuver les membres"),
            ("can_manage_communaute", "Peut gérer tous les membres"),
        ]

    def __str__(self):
        return f"{self.nom_entreprise} ({self.get_domaine_display()})"

    def save(self, *args, **kwargs):
        """Sauvegarde avec gestion du créateur"""
        if not self.pk and 'request' in kwargs:
            request = kwargs.pop('request')
            self.created_by = request.user
        super().save(*args, **kwargs)

    @property
    def can_be_edited_by(self, user):
        """Vérifie si l'utilisateur peut modifier cette entrée"""
        return user.is_authenticated and (
                user.is_staff
                or user == self.created_by
                or user.has_perm('communaute.can_manage_communaute')
        )