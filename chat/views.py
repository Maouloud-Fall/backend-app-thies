from rest_framework import generics, permissions, status
from rest_framework.response import Response
from chat.models import Message
from .serializers import MessageSerializer, CreateMessageSerializer
from django.db.models import Q

class MessageListCreateView(generics.ListCreateAPIView):
    """
    Vue pour lister les messages et en créer de nouveaux.
    - Utilise CreateMessageSerializer pour POST (création)
    - Utilise MessageSerializer pour GET (liste)
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return CreateMessageSerializer if self.request.method == 'POST' else MessageSerializer

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).order_by('-sent_at')

    def perform_create(self, serializer):
        """Assigne automatiquement l'expéditeur (sender) à l'utilisateur connecté"""
        serializer.save(sender=self.request.user)

class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vue pour récupérer, mettre à jour ou supprimer un message spécifique.
    - Marque automatiquement le message comme lu lors de la récupération
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'  # Explicitement défini pour plus de clarté

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(Q(sender=user) | Q(receiver=user))

    def retrieve(self, request, *args, **kwargs):
        """Marque le message comme lu lors de sa récupération"""
        instance = self.get_object()
        if instance.receiver == request.user:  # On ne marque comme lu que si le destinataire le consulte
            instance.mark_as_read()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class UnreadMessageCountView(generics.GenericAPIView):
    """
    Vue pour obtenir le nombre de messages non lus
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        count = Message.objects.filter(
            receiver=request.user,
            is_read=False
        ).count()
        return Response({'unread_count': count})