from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from .models import CustomUser
from .serializers import UserSerializer, RegisterSerializer, ProfileUpdateSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserList(generics.ListAPIView):
    """
    Vue pour lister tous les utilisateurs (admin seulement)
    """
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ['role', 'is_active']
    search_fields = ['username', 'email', 'full_name']

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Vue pour voir/modifier/supprimer un utilisateur spécifique
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_object(self):
        user = super().get_object()
        # Un utilisateur ne peut voir que son propre profil en détail
        if not (self.request.user.is_staff or user == self.request.user):
            raise PermissionDenied("Vous n'avez pas la permission d'accéder à ce profil")
        return user

class RegisterView(generics.CreateAPIView):
    """
    Vue pour l'inscription des nouveaux utilisateurs
    """
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        # Vous pouvez ajouter ici des actions post-création
        # comme l'envoi d'un email de bienvenue

class ProfileView(APIView):
    """
    Vue pour obtenir les informations du profil utilisateur
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response({
            'user': serializer.data,
            'status': 'online' if request.user.is_online else 'offline'
        })

class ProfileUpdateView(APIView):
    """
    Vue pour mettre à jour le profil utilisateur
    """
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        user = request.user
        serializer = ProfileUpdateSerializer(
            user,
            data=request.data,
            partial=True,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'Profil mis à jour avec succès',
                    'user': UserSerializer(user, context={'request': request}).data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'error': 'Erreur de validation',
                'details': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )