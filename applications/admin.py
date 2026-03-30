from django.contrib import admin
from django.utils.html import format_html
from .models import JobApplication


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    """Admin interface for JobApplication model."""
    
    list_display = [
        'company_name',
        'role',
        'date_applied',
        'status_badge',
        'job_type',
        'user',
        'created_at'
    ]
    
    list_filter = [
        'status',
        'job_type',
        'date_applied',
        'created_at',
        'user'
    ]
    
    search_fields = [
        'company_name',
        'role',
        'user__username',
        'response_notes'
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at',
        'days_since_applied',
        'is_follow_up_due'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'company_name', 'role', 'application_link')
        }),
        ('Application Details', {
            'fields': ('date_applied', 'job_type', 'ctc', 'resume_version')
        }),
        ('Status & Follow-up', {
            'fields': ('status', 'follow_up_date', 'is_follow_up_due')
        }),
        ('Notes & Response', {
            'fields': ('response_notes',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'days_since_applied'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        """Display status as colored badge."""
        colors = {
            'Applied': '#0dcaf0',
            'OA': '#0d6efd',
            'Shortlisted': '#0d6efd',
            'Interview': '#0dcaf0',
            'HR Round': '#6f42c1',
            'Rejected': '#dc3545',
            'Offer': '#198754',
            'Accepted': '#198754',
        }
        
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    ordering = ['-date_applied']
    date_hierarchy = 'date_applied'
