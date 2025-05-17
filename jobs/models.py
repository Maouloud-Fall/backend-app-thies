from django.db import models
from accounts.models import CustomUser


class Job(models.Model):
    JOB_TYPES = [
        ('CDD', 'Contrat à durée déterminée'),
        ('CDI', 'Contrat à durée indéterminée'),
        ('Freelance', 'Freelance'),
        ('Stage', 'Stage')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    employer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='posted_jobs'
    )
    location = models.CharField(max_length=255)
    job_type = models.CharField(
        max_length=10,
        choices=JOB_TYPES
    )
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    published_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-published_at']
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'

    def __str__(self):
        return f"{self.title} - {self.employer.username}"