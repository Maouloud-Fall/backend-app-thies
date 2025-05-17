from django.urls import path
from .views import ResourceListCreateView, ResourceRetrieveUpdateDestroyView

app_name = 'resources'

urlpatterns = [
    path('', ResourceListCreateView.as_view(), name='resource-list'),
    path('<int:pk>/', ResourceRetrieveUpdateDestroyView.as_view(), name='resource-detail'),
]