from django.urls import path
from .views import CommunauteListCreateView, CommunauteRetrieveUpdateDestroyView

urlpatterns = [
    path('communaute/', CommunauteListCreateView.as_view(), name='communaute-list'),
    path('communaute/<int:pk>/', CommunauteRetrieveUpdateDestroyView.as_view(), name='communaute-detail'),
]