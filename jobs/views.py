from rest_framework import generics, permissions
from .models import Job
from .serializers import JobSerializer
from accounts.permissions import IsEmployerOrReadOnly

class JobListCreateView(generics.ListCreateAPIView):
    queryset = Job.objects.filter(is_active=True)
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user)

class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsEmployerOrReadOnly]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()