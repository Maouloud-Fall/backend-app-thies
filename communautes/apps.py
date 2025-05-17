from django.apps import AppConfig

class CommunautesConfig(AppConfig):  # Le nom doit correspondre exactement
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'communautes'  # Doit matcher le nom du dossier
    verbose_name = "Communautés"  # Nom lisible