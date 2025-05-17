from rest_framework import serializers
from .models import Job
from accounts.serializers import UserSerializer

class JobSerializer(serializers.ModelSerializer):
    employer = UserSerializer(read_only=True)
    job_type_display = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'employer',
            'location', 'job_type', 'job_type_display',
            'salary', 'published_at', 'is_active'
        ]
        read_only_fields = ['employer', 'published_at']

    def get_job_type_display(self, obj):
        return obj.get_job_type_display()