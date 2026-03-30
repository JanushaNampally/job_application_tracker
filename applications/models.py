from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class JobApplication(models.Model):
    """
    Model to track job applications with comprehensive fields for tracking
    the complete hiring lifecycle from application to offer/rejection.
    """
    
    # Status choices for application tracking
    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('OA', 'Online Assessment'),
        ('Shortlisted', 'Shortlisted'),
        ('Interview', 'Interview'),
        ('HR Round', 'HR Round'),
        ('Rejected', 'Rejected'),
        ('Offer', 'Offer'),
        ('Accepted', 'Accepted'),
    ]
    
    # Job type choices
    JOB_TYPE_CHOICES = [
        ('Internship', 'Internship'),
        ('Full Time', 'Full Time'),
        ('Contract', 'Contract'),
        ('Remote', 'Remote'),
        ('Hybrid', 'Hybrid'),
        ('Onsite', 'Onsite'),
    ]
    
    # Core relationship and metadata
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications')
    
    # Application information
    company_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    date_applied = models.DateField(default=timezone.now)
    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPE_CHOICES,
        default='Full Time'
    )
    
    # Compensation information
    ctc = models.CharField(
        max_length=100,
        blank=True,
        default='',
        help_text='CTC/Stipend (e.g., 12 LPA, 50k/month)'
    )
    
    # Application tracking
    application_link = models.URLField(blank=True, max_length=500)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Applied'
    )
    
    # Follow-up tracking
    follow_up_date = models.DateField(null=True, blank=True)
    
    # Notes and responses
    response_notes = models.TextField(blank=True, default='')
    
    # Resume tracking
    resume_version = models.CharField(
        max_length=100,
        blank=True,
        default='',
        help_text='e.g., Resume_V1_AI_ML, Resume_V2_FullStack'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_applied']
        verbose_name = 'Job Application'
        verbose_name_plural = 'Job Applications'
        indexes = [
            models.Index(fields=['user', '-date_applied']),
            models.Index(fields=['user', 'status']),
            models.Index(fields=['follow_up_date']),
        ]
    
    def __str__(self):
        return f"{self.role} at {self.company_name} - {self.get_status_display()}"
    
    @property
    def is_follow_up_due(self):
        """Check if today is the follow-up date."""
        if self.follow_up_date:
            return self.follow_up_date == timezone.now().date()
        return False
    
    @property
    def days_since_applied(self):
        """Return number of days since application was submitted."""
        return (timezone.now().date() - self.date_applied).days
    
    @property
    def is_active(self):
        """Check if application is still in active status (not rejected/offer/accepted)."""
        inactive_statuses = ['Rejected', 'Offer', 'Accepted']
        return self.status not in inactive_statuses
