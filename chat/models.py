from django.db import models
from django.conf import settings
from django.utils import timezone

class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name="Expéditeur"
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages',
        verbose_name="Destinataire"
    )
    content = models.TextField(verbose_name="Contenu")
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'envoi"
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name="Lu"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_read']),
        ]

    def __str__(self):
        return f"Message de {self.sender} à {self.receiver} ({self.created_at})"

    def mark_as_read(self):
        """Marque le message comme lu et sauvegarde la modification"""
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])