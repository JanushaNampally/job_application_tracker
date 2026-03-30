from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    # Dashboard and Analytics
    path('', views.dashboard, name='dashboard'),
    path('analytics/', views.analytics, name='analytics'),
    
    # List and CRUD Views
    path('applications/', views.JobApplicationListView.as_view(), name='applications_list'),
    path('applications/<int:pk>/', views.JobApplicationDetailView.as_view(), name='application_detail'),
    path('create/', views.JobApplicationCreateView.as_view(), name='application_create'),
    path('applications/<int:pk>/edit/', views.JobApplicationUpdateView.as_view(), name='application_update'),
    path('applications/<int:pk>/delete/', views.JobApplicationDeleteView.as_view(), name='application_delete'),
    
    # API/AJAX Endpoints
    path('api/update-status/<int:pk>/', views.update_application_status, name='update_status'),
    path('api/quick-add/', views.quick_add_application, name='quick_add'),
    
    # Export Endpoints
    path('export/csv/', views.export_csv, name='export_csv'),
    path('export/excel/', views.export_excel, name='export_excel'),
    
    # Authentication
    path('register/', views.register, name='register'),
]
