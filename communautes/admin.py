from django.contrib import admin
from .models import Communaute

@admin.register(Communaute)
class CommunauteAdmin(admin.ModelAdmin):
    list_display = ('nom_entreprise', 'domaine', 'email', 'telephone')
    list_filter = ('domaine',)
    search_fields = ('nom_entreprise', 'email')
    ordering = ('nom_entreprise',)

    def has_view_permission(self, request, obj=None):
        return True  # Tous peuvent voir

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff  # Seuls les staffs peuvent modifier

    def has_delete_permission(self, request, obj=None):
        return request.user.is_staff  # Seuls les staffs peuvent supprimer