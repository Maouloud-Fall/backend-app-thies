from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils import timezone
from datetime import timedelta


class OnlineStatusFilter(admin.SimpleListFilter):
    title = 'Statut en ligne'
    parameter_name = 'online'

    def lookups(self, request, model_admin):
        return (
            ('online', 'En ligne'),
            ('offline', 'Hors ligne'),
        )

    def queryset(self, request, queryset):
        now = timezone.now()
        threshold = now - timedelta(minutes=5)
        if self.value() == 'online':
            return queryset.filter(last_activity__gte=threshold)
        if self.value() == 'offline':
            return queryset.exclude(last_activity__gte=threshold)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'phone',
                    'is_staff', 'is_active', 'is_online', 'last_activity_display')
    list_filter = (OnlineStatusFilter, 'role', 'is_staff', 'is_active', 'date_joined')
    readonly_fields = ('date_joined', 'last_login', 'last_activity', 'is_online_display')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {
            'fields': ('email', 'phone', 'birth_date', 'full_name')
        }),
        ('Statut', {
            'fields': ('is_online_display', 'last_activity'),
            'classes': ('collapse',),
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

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2',
                       'phone', 'birth_date', 'full_name', 'role'),
        }),
    )

    actions = ['activate_users', 'deactivate_users']

    @admin.display(boolean=True, description='En ligne')
    def is_online_display(self, obj):
        return obj.is_online

    @admin.display(description='Dernière activité')
    def last_activity_display(self, obj):
        if obj.last_activity:
            return obj.last_activity.strftime('%Y-%m-%d %H:%M:%S')
        return "Jamais"

    @admin.action(description='Activer les utilisateurs sélectionnés')
    def activate_users(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Désactiver les utilisateurs sélectionnés')
    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)