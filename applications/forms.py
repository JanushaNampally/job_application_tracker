from django import forms
from .models import JobApplication


class JobApplicationForm(forms.ModelForm):
    """Form for creating and editing job applications."""
    
    date_applied = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'required': 'required'
        }),
        label='Date Applied'
    )
    
    follow_up_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        required=False,
        label='Follow-up Date'
    )
    
    ctc = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 12 LPA or 50k/month'
        }),
        required=False,
        label='CTC / Stipend'
    )

    class Meta:
        model = JobApplication
        fields = [
            'company_name',
            'role',
            'date_applied',
            'job_type',
            'ctc',
            'application_link',
            'status',
            'follow_up_date',
            'resume_version',
            'response_notes',
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Google, Microsoft, Amazon',
                'required': 'required'
            }),
            'role': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Software Engineer, Data Scientist',
                'required': 'required'
            }),
            'job_type': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
            'application_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://careers.example.com/job/123'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
            'resume_version': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Resume_V1_AI_ML, Resume_V2_FullStack'
            }),
            'response_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'HR Response / OA Link / Interview Feedback / Recruiter Messages'
            }),
        }
        labels = {
            'company_name': 'Company Name',
            'role': 'Job Role',
            'date_applied': 'Date Applied',
            'job_type': 'Job Type',
            'application_link': 'Application Link',
            'status': 'Current Status',
            'resume_version': 'Resume Version Used',
            'response_notes': 'Response / Notes',
        }


class QuickApplicationForm(forms.ModelForm):
    """Quick entry form for rapid application logging - modal popup."""
    
    date_applied = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control form-control-sm'
        }),
        label='Date Applied'
    )

    class Meta:
        model = JobApplication
        fields = [
            'company_name',
            'role',
            'date_applied',
            'job_type',
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Company name'
            }),
            'role': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Job role'
            }),
            'job_type': forms.Select(attrs={
                'class': 'form-select form-select-sm'
            }),
        }


class JobApplicationFilterForm(forms.Form):
    """Form for filtering job applications."""
    
    company = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by company...'
        })
    )
    
    role = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by role...'
        })
    )
    
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All Statuses')] + list(JobApplication.STATUS_CHOICES),
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    job_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All Types')] + list(JobApplication.JOB_TYPE_CHOICES),
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    resume_version = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filter by resume version...'
        })
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
