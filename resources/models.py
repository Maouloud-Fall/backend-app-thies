from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class Resource(models.Model):
    class Category(models.TextChoices):
        FORMATION = 'formation', 'Formation'
        ORIENTATION = 'orientation', 'Orientation'
        ACTUALITES = 'actualités', 'Actualités'
        CONSEILS = 'conseils', 'Conseils'

    title = models.CharField(max_length=255, verbose_name="Titre")
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        verbose_name="Slug (URL)",
        help_text="Ce champ est généré automatiquement à partir du titre"
    )
    content = models.TextField(verbose_name="Contenu")
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        verbose_name="Catégorie"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    is_published = models.BooleanField(default=True, verbose_name="Publié")

    class Meta:
        verbose_name = "Ressource"
        verbose_name_plural = "Ressources"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['created_at']),
            models.Index(fields=['slug']),  # Nouvel index pour le slug
        ]

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Assure l'unicité du slug
            original_slug = self.slug
            counter = 1
            while Resource.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)