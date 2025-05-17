from rest_framework import serializers
from .models import Communaute

class CommunauteSerializer(serializers.ModelSerializer):
    domaine_display = serializers.CharField(
        source='get_domaine_display',
        read_only=True
    )

    class Meta:
        model = Communaute
        fields = [
            'id',
            'nom_entreprise',
            'adresse',
            'telephone',
            'email',
            'domaine',
            'domaine_display',
            'site_web',
            'date_creation'
        ]
        read_only_fields = ['date_creation']