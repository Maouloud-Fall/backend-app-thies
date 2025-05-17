from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'applicant', 'job', 'status', 'applied_at')
    list_filter = ('status', 'job__job_type')
    search_fields = ('applicant__username', 'job__title')
    readonly_fields = ('applied_at', 'updated_at')