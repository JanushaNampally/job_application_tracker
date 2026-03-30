# Job Application Tracker 🎯

> **Professional-Grade Job Hunt Management Platform**
> 
> A production-ready Django web application for tracking job applications with sophisticated analytics, smart filters, and automatic follow-up reminders. Built for both quick entry and comprehensive tracking.

## ✨ Features

### Core Features
- 🔐 **User Authentication**: Secure registration, login, and logout system
- 📝 **Complete Application Tracking**: Track 10+ fields per application
- 📊 **Dashboard**: Real-time statistics and visual analytics
- 🔍 **Smart Filters**: Filter by company, role, status, job type, date range, and resume version
- 📈 **Analytics**: Comprehensive charts and insights into your job hunt progress
- ⚡ **Quick Add Modal**: Lightning-fast application entry with popup form
- 🔔 **Follow-up Reminders**: Automatic reminders for pending follow-ups
- 📲 **Responsive Design**: Perfect on desktop, tablet, and mobile
- 💾 **Export Options**: Export to CSV and Excel formats
- 🎨 **Professional UI**: Modern SaaS-style dashboard with Bootstrap 5

### Advanced Features
- **Status Update Workflow**: Direct status updates from table view via dropdown
- **Resume Version Tracking**: Track and filter by different resume versions
- **Response/Notes System**: Store HR responses, OA links, interview feedback
- **Application Lifecycle Management**: Track from Applied to Accepted status
- **Time-Based Analytics**: Monitor your application patterns over time
- **Company-Wise Analytics**: See which companies have received your applications
- **Job Type Distribution**: Analyze your job preferences

## 🏗️ Project Structure

```
job_application_tracker/
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── db.sqlite3                         # SQLite database
│
├── job_application_tracker/           # Project settings
│   ├── settings.py                   # Django configuration
│   ├── urls.py                       # URL routing
│   ├── wsgi.py                       # WSGI application
│   └── asgi.py                       # ASGI application
│
├── applications/                      # Main Django app
│   ├── models.py                     # Database models
│   ├── views.py                      # View logic
│   ├── forms.py                      # Form definitions
│   ├── urls.py                       # App URL routing
│   ├── admin.py                      # Django admin config
│   ├── apps.py                       # App configuration
│   │
│   ├── templatetags/                 # Custom template filters
│   │   ├── __init__.py
│   │   └── custom_filters.py
│   │
│   └── templates/applications/       # Application templates
│       ├── dashboard.html             # Main dashboard
│       ├── applications_list.html      # All applications list
│       ├── application_form.html       # Add/Edit form
│       ├── application_detail.html     # Single application view
│       ├── application_confirm_delete.html  # Delete confirmation
│       └── analytics.html              # Analytics dashboard
│
├── templates/                         # Global templates
│   ├── base.html                     # Base template
│   └── registration/
│       ├── login.html                # Login page
│       └── register.html             # Registration page
│
├── static/                            # Static files
│   ├── css/
│   │   └── style.css                 # Custom styles
│   └── js/
│       └── main.js                   # Custom JavaScript
│
└── logs/                              # Application logs
    └── debug.log                      # Debug logs
```

## 🚀 Quick Start

### 1. Installation

```bash
# Navigate to project directory
cd job_application_tracker

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Create database tables
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser
# Follow prompts to create admin account
```

### 3. Run Development Server

```bash
python manage.py runserver

# Server will be available at: http://127.0.0.1:8000
```

### 4. Access the Application

- 🌐 **Main App**: http://127.0.0.1:8000
- 👨‍💼 **Admin Panel**: http://127.0.0.1:8000/admin

## 📖 Usage Guide

### Creating First Application
1. Click "Quick Add" button on dashboard or "Add Application" in navigation
2. Fill in basic information (Company, Role, Date, Job Type)
3. Click "Add" - saved immediately!

### Full Application Entry
1. Go to "Add Application" page
2. Fill in all fields including CTC, links, notes
3. Set follow-up date for reminders

### Viewing and Managing
1. **Dashboard**: Get overview of all applications with key metrics
2. **All Applications**: View, edit, delete, or filter applications
3. **Analytics**: See charts and detailed statistics
4. **Export**: Download data as CSV or Excel

### Filtering Applications
- Use company/role search for quick lookup
- Filter by status to see specific stages
- Filter by job type or date range
- Filter by resume version used

### Status Management
- Click on status dropdown to update directly from list view
- Status options: Applied, OA, Shortlisted, Interview, HR Round, Rejected, Offer, Accepted
- Changes save immediately via AJAX

## 🔧 Django Management Commands

```bash
# Collect static files
python manage.py collectstatic

# Check project status
python manage.py check

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Access Django shell
python manage.py shell

# Show all URLs
python manage.py show_urls
```

## 📊 Model Fields

### JobApplication Model

| Field | Type | Purpose |
|-------|------|---------|
| user | ForeignKey | Links to user account |
| company_name | CharField | Company hiring for |
| role | CharField | Job position/title |
| date_applied | DateField | When you applied |
| job_type | CharField | Type (Internship, Full-time, etc.) |
| ctc | CharField | Compensation (optional) |
| application_link | URLField | Job posting link |
| status | CharField | Current status in pipeline |
| follow_up_date | DateField | When to follow up |
| response_notes | TextField | Notes/feedback/responses |
| resume_version | CharField | Which resume version used |
| created_at | DateTimeField | Record creation timestamp |
| updated_at | DateTimeField | Last modification timestamp |

## 🔐 Authentication

- **Registration**: Create new account with secure password validation
- **Login**: Access your personal application history
- **Permissions**: Users only see their own applications
- **Security**: CSRF protection, SQL injection prevention

## 📱 Responsive Design

- ✅ Desktop (1920x1080)
- ✅ Tablet (768px)
- ✅ Mobile (320px)
- Bootstrap 5 grid system for perfect alignment

## 🎨 Styling

- **Primary Color**: #0d6efd (Blue)
- **Bootstrap 5.3**: Modern, professional components
- **Bootstrap Icons**: Rich icon library
- **Custom CSS**: Enhanced styling and animations
- **Dark Mode Support**: Ready for CSS theming

## 📈 Analytics Features

- **Status Distribution**: Pie chart of applications by status
- **Job Type Analysis**: Bar chart of job type preferences
- **Monthly Trends**: Line chart of applications over time
- **Company Analysis**: Top 10 companies targeting
- **Resume Performance**: Which resume versions are used most
- **Success Metrics**: Track conversion rates

## 🔔 Follow-up Reminder System

- Set follow-up date when adding application
- Dashboard shows count of pending follow-ups
- Red/yellow highlighting for applications due today
- Banner alert on dashboard for reminders

## 💾 Export Features

- **CSV Export**: Compatible with Excel, Google Sheets
- **Excel Export**: Formatted with colors, styling
- **All Data**: Exports all visible applications
- **Filtered Export**: Export filtered results

## 🛡️ Security Features

- Django's built-in CSRF protection
- SQL injection prevention via ORM
- Secure password hashing (PBKDF2)
- User isolation (each sees only their data)
- HTTPS ready (configure in production)
- XSS protection via template escaping

## ⚙️ Configuration

### Environment Variables (Optional)
Create `.env` file:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database (Change from SQLite)
Edit `settings.py` DATABASES section for PostgreSQL/MySQL

### Email Configuration (Optional)
For production deployment with email notifications

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG = False` in settings.py
- [ ] Generate secure `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up database (PostgreSQL recommended)
- [ ] Configure static files collection
- [ ] Set up SSL/HTTPS
- [ ] Configure backup strategy
- [ ] Set up logging

### Deploy to Heroku
```bash
# Install Heroku CLI
# Create Heroku app
heroku create your-app-name

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate
```

## 📝 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | / | Dashboard  |
| GET | /applications/ | List all applications |
| POST | /create/ | Create new application |
| GET | /applications/<id>/ | View single application |
| POST | /applications/<id>/edit/ | Update application |
| POST | /applications/<id>/delete/ | Delete application |
| POST | /api/update-status/<id>/ | Update status (AJAX) |
| POST | /api/quick-add/ | Quick add (AJAX) |
| GET | /analytics/ | Analytics dashboard |
| GET | /export/csv/ | Export as CSV |
| GET | /export/excel/ | Export as Excel |

## 🐛 Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Database Locked
```bash
rm db.sqlite3
python manage.py migrate
```

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### Import Errors
```bash
pip install -r requirements.txt --force-reinstall
```

## 📚 Technologies & Libraries

- **Django 5.1**: Web framework
- **Bootstrap 5.3**: UI components
- **Bootstrap Icons**: Icon library
- **Chart.js**: Analytics charts
- **openpyxl**: Excel export
- **Python 3.8+**: Language

## 🎓 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [Chart.js Documentation](https://www.chartjs.org/)
- [Python Tutorial](https://docs.python.org/3/)

##  Contributing

Feel free to fork, modify, and enhance this project!

## 📄 License

Open source - Use freely for personal and professional projects

## 💡 Future Enhancements

- [ ] Email notifications for follow-ups
- [ ] Interview scheduling integration
- [ ] Resume auto-tagging with AI
- [ ] Mobile app
- [ ] Dark mode theme
- [ ] Advanced filtering (compound filters)
- [ ] Interview feedback scoring
- [ ] Company ratings/reviews
- [ ] Salary history tracking
- [ ] Multi-language support

## 👨‍💻 Author Notes

This application is designed to be:
- ✅ **Production-ready**: Can deploy immediately
- ✅ **Portfolio-worthy**: Shows full-stack Django skills
- ✅ **Extensible**: Easy to add features
- ✅ **Professional**: Enterprise-quality code
- ✅ **Scalable**: Database-ready for growth

---

**Happy job hunting!** 🚀

For issues or questions, check the documentation or create an issue.

**Last Updated**: March 2026
**Version**: 1.0.0


4. **Navigate to Project Directory**
   ```
   cd job_application_tracker
   ```

5. **Run Database Migrations**
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a Superuser (Optional, for admin access)**
   ```
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin user.

7. **Run the Development Server**
   ```
   python manage.py runserver
   ```

8. **Access the Application**
   - Open your browser and go to: `http://127.0.0.1:8000/`
   - Register a new account or login if you have one

## Usage

### For Regular Users

1. **Register/Login**: Create an account or login with existing credentials
2. **Dashboard**: View all your job applications in a table format
3. **Add Application**: Click "Add Application" to create a new job application entry
4. **Edit Application**: Click "Edit" next to any application to update its details
5. **Delete Application**: Click "Delete" to remove an application (with confirmation)
6. **Filter Applications**: Use the filter options to view applications by status or company

### Automated Status Updates

To automatically update old applications to "Rejected" status (useful for maintenance):

```
python manage.py update_statuses --days=30
```

This will mark applications that haven't been updated in 30 days and are still "Applied" as "Rejected".

## Project Structure

```
job_application_tracker/
├── job_application_tracker/     # Main project settings
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── applications/                # Main app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── management/
│   │   └── commands/
│   │       └── update_statuses.py
│   └── templates/
│       └── applications/
│           ├── application_form.html
│           ├── confirm_delete.html
│           └── dashboard.html
├── templates/                   # Global templates
│   ├── base.html
│   └── registration/
│       ├── login.html
│       └── register.html
├── db.sqlite3                   # Database file
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Customization

### Changing Status Options

Edit `applications/models.py` to modify the `STATUS_CHOICES` in the `JobApplication` model.

### Styling

The application uses Bootstrap for styling. Customize `templates/base.html` to change the overall look and feel.

### Database

By default, the app uses SQLite. To use PostgreSQL or MySQL, update `settings.py` with your database configuration.

## Security Features

- CSRF protection on all forms
- User authentication required for all application management
- Secure password hashing
- SQL injection protection through Django ORM

## Deployment

For production deployment:

1. Set `DEBUG = False` in `settings.py`
2. Configure a production database
3. Set up static file serving
4. Use a WSGI server like Gunicorn
5. Configure HTTPS

## Contributing

This project demonstrates Django best practices and can be extended with:

- Email notifications for status changes
- Resume upload functionality
- Interview scheduling features
- Analytics dashboard
- API endpoints for mobile app integration

## License

This project is open-source and available under the MIT License.

## Author

Built as a portfolio project for demonstrating Django and web development skills in an AI/ML engineer context.
