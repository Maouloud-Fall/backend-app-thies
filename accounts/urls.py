from django.urls import path
from .views import UserList, UserDetail, RegisterView, ProfileView, ProfileUpdateView

urlpatterns = [
    path('users/', UserList.as_view(), name='user-list'),  # GET /accounts/users/
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),  # GET/PUT/PATCH/DELETE /accounts/users/{id}
    path('register/', RegisterView.as_view(), name='register'),  # POST /accounts/register/
    path('profile/', ProfileView.as_view(), name='profile'),  # GET /accounts/profile/
    path('profile/update/', ProfileUpdateView.as_view(), name='profile-update'),  # PATCH /accounts/profile/update/
]