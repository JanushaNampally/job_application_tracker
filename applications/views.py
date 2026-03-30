import csv
import json
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.utils import timezone
from .models import JobApplication
from .forms import JobApplicationForm, QuickApplicationForm, JobApplicationFilterForm


# ========================= DASHBOARD VIEWS =========================

@login_required
def dashboard(request):
    """Main dashboard showing overview and statistics."""
    user_applications = JobApplication.objects.filter(user=request.user)
    
    # Calculate statistics
    total_applications = user_applications.count()
    applied = user_applications.filter(status='Applied').count()
    oas = user_applications.filter(status='OA').count()
    shortlisted = user_applications.filter(status='Shortlisted').count()
    interviews = user_applications.filter(status='Interview').count()
    hr_rounds = user_applications.filter(status='HR Round').count()
    rejected = user_applications.filter(status='Rejected').count()
    offers = user_applications.filter(status='Offer').count()
    accepted = user_applications.filter(status='Accepted').count()
    
    # Pending follow-ups
    today = timezone.now().date()
    pending_followups = user_applications.filter(
        follow_up_date__lte=today,
        status__in=['Applied', 'OA', 'Shortlisted', 'Interview', 'HR Round']
    ).count()
    
    # Recent applications (last 7 days)
    week_ago = today - timedelta(days=7)
    recent_applications = user_applications.filter(
        date_applied__gte=week_ago
    ).order_by('-date_applied')[:5]
    
    # Applications by job type
    job_type_stats = user_applications.values('job_type').annotate(count=Count('id'))
    
    # Applications by status for the current month
    month_start = today.replace(day=1)
    current_month_apps = user_applications.filter(date_applied__gte=month_start)
    
    context = {
        'total_applications': total_applications,
        'applied': applied,
        'oas': oas,
        'shortlisted': shortlisted,
        'interviews': interviews,
        'hr_rounds': hr_rounds,
        'rejected': rejected,
        'offers': offers,
        'accepted': accepted,
        'pending_followups': pending_followups,
        'recent_applications': recent_applications,
        'job_type_stats': list(job_type_stats),
        'current_month_count': current_month_apps.count(),
    }
    
    return render(request, 'applications/dashboard.html', context)


@login_required
def analytics(request):
    """Analytics page with charts and detailed statistics."""
    user_applications = JobApplication.objects.filter(user=request.user)
    
    # Status distribution
    status_data = user_applications.values('status').annotate(count=Count('id')).order_by('-count')
    
    # Job type distribution
    job_type_data = user_applications.values('job_type').annotate(count=Count('id')).order_by('-count')
    
    # Applications by month (last 6 months)
    today = timezone.now().date()
    six_months_ago = today - timedelta(days=180)
    monthly_data = {}
    
    for i in range(6):
        month_date = today - timedelta(days=30 * (5 - i))
        month_key = month_date.strftime('%b %Y')
        month_start = month_date.replace(day=1)
        if i == 0:  # Current month
            month_end = today
        else:
            month_end = month_date.replace(day=1) + timedelta(days=32)
            month_end = month_end.replace(day=1) - timedelta(days=1)
        
        count = user_applications.filter(
            date_applied__gte=month_start,
            date_applied__lte=month_end
        ).count()
        monthly_data[month_key] = count
    
    # Company-wise applications (top 10)
    company_data = user_applications.values('company_name').annotate(count=Count('id')).order_by('-count')[:10]
    
    # Resume version usage
    resume_version_data = user_applications.exclude(resume_version='').values('resume_version').annotate(count=Count('id')).order_by('-count')
    
    # Resume version stats
    total_with_resume = user_applications.exclude(resume_version='').count()
    
    context = {
        'status_data': list(status_data),
        'job_type_data': list(job_type_data),
        'monthly_data': monthly_data,
        'company_data': list(company_data),
        'resume_version_data': list(resume_version_data),
        'total_with_resume': total_with_resume,
        'total_applications': user_applications.count(),
    }
    
    return render(request, 'applications/analytics.html', context)


# ========================= CRUD VIEWS =========================

class JobApplicationListView(LoginRequiredMixin, ListView):
    """Class-based view to list all job applications with filtering."""
    model = JobApplication
    template_name = 'applications/applications_list.html'
    context_object_name = 'applications'
    paginate_by = 15
    
    def get_queryset(self):
        queryset = JobApplication.objects.filter(user=self.request.user).order_by('-date_applied')
        
        # Get filter parameters
        company = self.request.GET.get('company')
        role = self.request.GET.get('role')
        status = self.request.GET.get('status')
        job_type = self.request.GET.get('job_type')
        resume_version = self.request.GET.get('resume_version')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        
        # Apply filters
        if company:
            queryset = queryset.filter(company_name__icontains=company)
        if role:
            queryset = queryset.filter(role__icontains=role)
        if status:
            queryset = queryset.filter(status=status)
        if job_type:
            queryset = queryset.filter(job_type=job_type)
        if resume_version:
            queryset = queryset.filter(resume_version__icontains=resume_version)
        if date_from:
            queryset = queryset.filter(date_applied__gte=date_from)
        if date_to:
            queryset = queryset.filter(date_applied__lte=date_to)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = JobApplicationFilterForm(self.request.GET)
        
        # Add follow-up reminders
        today = timezone.now().date()
        context['followup_reminders'] = JobApplication.objects.filter(
            user=self.request.user,
            follow_up_date=today
        )
        
        return context


class JobApplicationDetailView(LoginRequiredMixin, DetailView):
    """View to display details of a single application."""
    model = JobApplication
    template_name = 'applications/application_detail.html'
    context_object_name = 'application'
    
    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)


class JobApplicationCreateView(LoginRequiredMixin, CreateView):
    """View to create a new job application."""
    model = JobApplication
    form_class = JobApplicationForm
    template_name = 'applications/application_form.html'
    success_url = reverse_lazy('applications_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Job application added successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Job Application'
        return context


class JobApplicationUpdateView(LoginRequiredMixin, UpdateView):
    """View to update an existing job application."""
    model = JobApplication
    form_class = JobApplicationForm
    template_name = 'applications/application_form.html'
    success_url = reverse_lazy('applications_list')
    
    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Job application updated successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Job Application'
        return context


class JobApplicationDeleteView(LoginRequiredMixin, DeleteView):
    """View to delete a job application."""
    model = JobApplication
    template_name = 'applications/application_confirm_delete.html'
    success_url = reverse_lazy('applications_list')
    
    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Job application deleted successfully!')
        return super().delete(request, *args, **kwargs)


# ========================= AJAX/API VIEWS =========================

@login_required
def update_application_status(request, pk):
    """AJAX endpoint to update application status directly from table."""
    if request.method == 'POST':
        try:
            application = get_object_or_404(JobApplication, pk=pk, user=request.user)
            new_status = request.POST.get('status')
            
            if new_status in dict(JobApplication.STATUS_CHOICES):
                application.status = new_status
                application.save()
                return JsonResponse({
                    'success': True,
                    'message': f'Status updated to {new_status}'
                })
            else:
                return JsonResponse({'success': False, 'message': 'Invalid status'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


@login_required
def quick_add_application(request):
    """AJAX endpoint for quick application entry (modal)."""
    if request.method == 'POST':
        form = QuickApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            return JsonResponse({
                'success': True,
                'message': 'Application added successfully!',
                'application_id': application.id
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


# ========================= EXPORT VIEWS =========================

@login_required
def export_csv(request):
    """Export all applications as CSV file."""
    applications = JobApplication.objects.filter(user=request.user).order_by('-date_applied')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="job_applications.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Company Name',
        'Role',
        'Date Applied',
        'Job Type',
        'CTC/Stipend',
        'Status',
        'Follow-up Date',
        'Resume Version',
        'Application Link',
        'Response Notes',
        'Days Since Applied'
    ])
    
    for app in applications:
        writer.writerow([
            app.company_name,
            app.role,
            app.date_applied.strftime('%Y-%m-%d'),
            app.job_type,
            app.ctc or '',
            app.status,
            app.follow_up_date.strftime('%Y-%m-%d') if app.follow_up_date else '',
            app.resume_version or '',
            app.application_link or '',
            app.response_notes or '',
            app.days_since_applied
        ])
    
    return response


@login_required
def export_excel(request):
    """Export all applications as Excel file."""
    try:
        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    except ImportError:
        messages.error(request, 'Excel export requires openpyxl package')
        return redirect('applications_list')
    
    applications = JobApplication.objects.filter(user=request.user).order_by('-date_applied')
    
    # Create workbook and sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Job Applications'
    
    # Set column widths
    columns = [20, 20, 15, 15, 15, 15, 15, 20, 30, 30, 15]
    for idx, width in enumerate(columns, start=1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(idx)].width = width
    
    # Header styling
    headers = [
        'Company Name', 'Role', 'Date Applied', 'Job Type', 'CTC/Stipend',
        'Status', 'Follow-up Date', 'Resume Version', 'Application Link',
        'Response Notes', 'Days Since Applied'
    ]
    
    header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
    header_font = Font(bold=True, color='FFFFFF')
    header_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    for col_idx, header in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col_idx)
        cell.value = header
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = header_alignment
        cell.border = thin_border
    
    # Add data rows
    status_colors = {
        'Applied': 'E2EFDA',
        'OA': 'D9E1F2',
        'Shortlisted': 'D9E1F2',
        'Interview': 'E2EFDA',
        'HR Round': 'E4DFEC',
        'Rejected': 'F4CCCC',
        'Offer': 'D9EAD3',
        'Accepted': 'D9EAD3',
    }
    
    for row_idx, app in enumerate(applications, start=2):
        row_fill = PatternFill(start_color=status_colors.get(app.status, 'FFFFFF'),
                              end_color=status_colors.get(app.status, 'FFFFFF'),
                              fill_type='solid')
        
        row_data = [
            app.company_name,
            app.role,
            app.date_applied.strftime('%Y-%m-%d'),
            app.job_type,
            app.ctc or '',
            app.status,
            app.follow_up_date.strftime('%Y-%m-%d') if app.follow_up_date else '',
            app.resume_version or '',
            app.application_link or '',
            app.response_notes or '',
            app.days_since_applied
        ]
        
        for col_idx, value in enumerate(row_data, start=1):
            cell = ws.cell(row=row_idx, column=col_idx)
            cell.value = value
            cell.fill = row_fill
            cell.border = thin_border
            if col_idx in [3, 6, 7, 11]:  # Center align date and status columns
                cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            else:
                cell.alignment = Alignment(vertical='center', wrap_text=True)
    
    # Add summary sheet
    summary_ws = wb.create_sheet('Summary')
    status_summary = applications.values('status').annotate(count=Count('id'))
    
    summary_ws['A1'].value = 'Status Summary'
    summary_ws['A1'].font = Font(bold=True, size=12)
    summary_ws['A2'].value = 'Status'
    summary_ws['B2'].value = 'Count'
    
    for idx, item in enumerate(status_summary, start=3):
        summary_ws[f'A{idx}'].value = item['status']
        summary_ws[f'B{idx}'].value = item['count']
    
    # Save file
    filename = f'job_applications_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    wb.save(response)
    
    return response


# ========================= AUTHENTICATION VIEWS =========================

def register(request):
    """User registration view."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


def custom_login(request):
    """Custom login view with message support."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    return redirect('login')
