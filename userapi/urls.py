from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from accounts.views import UserList, UserDetail, RegisterView

urlpatterns = [
    # Page d'accueil
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    # Admin
    path('admin/', admin.site.urls),

    # API Users
    path('api/users/', UserList.as_view(), name='user-list'),
    path('api/users/<int:pk>/', UserDetail.as_view(), name='user-detail'),

    # Authentification
    path('api/auth/', include([
        path('register/', RegisterView.as_view(), name='register'),
        path('', include('rest_framework.urls')),  # Login/logout DRF
    ])),

    # API Jobs
    path('api/jobs/', include('jobs.urls')),  # Intégration des URLs des jobs

    #API applications
    path('api/applications/', include('applications.urls')),

    #API ressources
    path('api/resources/', include('resources.urls')),

    #API messages
    path('api/chat/', include('chat.urls')),

    # Documentation API
    path('api/docs/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
]