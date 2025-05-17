from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Gestion personnalisée des utilisateurs dans l'interface d'administration."""

    # Affichage de la liste des utilisateurs
    list_display = ('username', 'email', 'role', 'phone', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'phone')
    ordering = ('username', '-date_joined')  # Trie par nom complet

    readonly_fields = ('date_joined', 'last_login')

    # Configuration du formulaire d'édition
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {
            'fields': ('email', 'phone', 'birth_date')
        }),
        ('Rôles et permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions'),
        }),
        ('Dates importantes', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )

    # Configuration du formulaire de création
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'phone', 'birth_date', 'role'),
        }),
    )

    # Actions personnalisées
    actions = ['activate_users', 'deactivate_users']

    @admin.action(description='Activer les utilisateurs sélectionnés')
    def activate_users(self, request, queryset):
        """Active les comptes des utilisateurs sélectionnés."""
        queryset.update(is_active=True)
        self.message_user(request, "Les utilisateurs sélectionnés ont été activés.")

    @admin.action(description='Désactiver les utilisateurs sélectionnés')
    def deactivate_users(self, request, queryset):
        """Désactive les comptes des utilisateurs sélectionnés."""
        queryset.update(is_active=False)
        self.message_user(request, "Les utilisateurs sélectionnés ont été désactivés.")