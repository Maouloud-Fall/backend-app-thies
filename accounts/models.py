from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        EMPLOYER = "EMPLOYER", "Employer"
        USER = "USER", "User"

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.USER)
    phone = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    full_name = models.CharField(max_length=150, blank=True)
    last_activity = models.DateTimeField(null=True, blank=True)

    @property
    def is_online(self):
        if self.last_activity:
            return timezone.now() - self.last_activity < timedelta(minutes=5)
        return False

    def save(self, *args, **kwargs):
        if self.full_name:
            if len(self.full_name.split()) < 2:
                raise ValueError("Le nom d'utilisateur doit contenir un prénom et un nom.")
            self.username = self.full_name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name if self.full_name else self.username