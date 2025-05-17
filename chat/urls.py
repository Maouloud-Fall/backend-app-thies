from django.urls import path
from .views import MessageListCreateView, MessageDetailView, UnreadMessageCountView

app_name = 'messages'

urlpatterns = [
    path('messages/', MessageListCreateView.as_view(), name='message-list'),
    path('<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
    path('unread-count/', UnreadMessageCountView.as_view(), name='unread-count'),
]