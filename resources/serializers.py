from rest_framework import serializers
from .models import Resource

class ResourceSerializer(serializers.ModelSerializer):
    category_display = serializers.SerializerMethodField()

    class Meta:
        model = Resource
        fields = [
            'id', 'title', 'content',
            'category', 'category_display',
            'created_at', 'updated_at', 'is_published'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_category_display(self, obj):
        return obj.get_category_display()