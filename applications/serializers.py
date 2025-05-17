from rest_framework import serializers
from .models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    applicant = serializers.StringRelatedField(read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = [
            'id', 'job', 'job_title', 'applicant',
            'cover_letter', 'status', 'status_display',
            'applied_at', 'updated_at'
        ]
        read_only_fields = ['applicant', 'applied_at', 'updated_at']

    def get_status_display(self, obj):
        return obj.get_status_display()