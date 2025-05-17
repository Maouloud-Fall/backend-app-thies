from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """Modèle utilisateur personnalisé avec nom complet en tant que username."""

    # Types d'utilisateurs
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        EMPLOYER = "EMPLOYER", "Employer"
        USER = "USER", "User"

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.USER)
    phone = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    full_name = models.CharField(max_length=150, blank=True)  # Nom long avec espaces autorisés

    # Propriété pratique pour vérifier si l'utilisateur est un employeur
    @property
    def is_employer(self):
        return self.role == self.Role.EMPLOYER

    def save(self, *args, **kwargs):
        """S'assure que full_name est utilisé comme username avec validation."""
        if self.full_name:
            if len(self.full_name.split()) < 2:
                raise ValueError("Le nom d'utilisateur doit contenir un prénom et un nom.")
            self.username = self.full_name  # Assigne full_name à username
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name if self.full_name else self.username  # Retourne full_name s'il est défini