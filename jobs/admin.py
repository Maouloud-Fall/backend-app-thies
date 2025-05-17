from django.contrib import admin
from .models import Job

class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'job_type', 'location', 'salary', 'published_at', 'is_active')
    list_filter = ('job_type', 'location', 'is_active')
    search_fields = ('title', 'description', 'employer__username')
    readonly_fields = ('published_at',)
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'employer')
        }),
        ('Détails', {
            'fields': ('location', 'job_type', 'salary')
        }),
        ('Dates/Statut', {
            'fields': ('published_at', 'is_active')
        }),
    )

admin.site.register(Job, JobAdmin)