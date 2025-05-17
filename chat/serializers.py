from rest_framework import serializers
from chat.models import Message
from accounts.serializers import UserSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'id', 'sender', 'receiver',
            'content', 'sent_at', 'is_read'
        ]
        read_only_fields = ['sender', 'sent_at']

class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'  # ou spécifiez les champs nécessaires (ex: ['content', 'receiver'])