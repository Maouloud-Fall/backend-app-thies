from rest_framework import generics, permissions
from .models import Communaute
from .serializers import CommunauteSerializer

class CommunauteListCreateView(generics.ListCreateAPIView):
    serializer_class = CommunauteSerializer
    permission_classes = [permissions.IsAuthenticated]  # Seulement pour utilisateurs connectés

    def get_queryset(self):
        # Tout le monde peut voir les communautés
        return Communaute.objects.all()

    def perform_create(self, serializer):
        # Associe automatiquement l'utilisateur connecté
        serializer.save(proprietaire=self.request.user)

class CommunauteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Communaute.objects.all()
    serializer_class = CommunauteSerializer
    permission_classes = [permissions.IsAuthenticated]  # Modification réservée

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]  # Lecture ouverte à tous
        return [permissions.IsAuthenticated()]  # Écriture réservée