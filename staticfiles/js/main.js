/**
 * Job Application Tracker - Main JavaScript
 * Handles interactive features and AJAX operations
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        initializeTooltips();
    }

    // Initialize status selects
    initializeStatusSelects();

    // Initialize search/filter
    initializeFilters();
});

/**
 * Initialize Bootstrap Tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize Status Select Dropdowns with AJAX
 */
function initializeStatusSelects() {
    const statusSelects = document.querySelectorAll('.status-select');
    
    statusSelects.forEach(select => {
        select.addEventListener('change', function() {
            const appId = this.dataset.appId;
            const newStatus = this.value;
            updateApplicationStatus(appId, newStatus);
        });
    });
}

/**
 * Update Application Status via AJAX
 */
function updateApplicationStatus(appId, status) {
    const csrfToken = getCsrfToken();
    const formData = new FormData();
    formData.append('status', status);

    fetch(`/api/update-status/${appId}/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('Status updated successfully!', 'success');
            // Reload row or update UI
            setTimeout(() => location.reload(), 500);
        } else {
            showAlert('Error: ' + data.message, 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('An error occurred. Please try again.', 'danger');
    });
}

/**
 * Get CSRF Token from Cookie
 */
function getCsrfToken() {
    return document.querySelector('input[name="csrfmiddlewaretoken"]')?.value || 
           document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
}

/**
 * Show Alert Notification
 */
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

/**
 * Initialize Filter Form
 */
function initializeFilters() {
    const form = document.querySelector('form[method="get"]');
    if (!form) return;

    // Auto-submit on certain changes
    const selects = form.querySelectorAll('select, input[type="date"]');
    selects.forEach(control => {
        control.addEventListener('change', function() {
            // Optional: Auto-submit on change
            // form.submit();
        });
    });
}

/**
 * Format Date Helper
 */
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

/**
 * Highlight Follow-up Due Rows
 */
function highlightFollowupDueRows() {
    const today = new Date().toISOString().split('T')[0];
    const rows = document.querySelectorAll('table tbody tr');
    
    rows.forEach(row => {
        const followupCell = row.querySelector('[data-followup-date]');
        if (followupCell && followupCell.dataset.followupDate === today) {
            row.classList.add('table-warning');
        }
    });
}

/**
 * Export Functionality
 */
function handleExport(format) {
    const form = document.createElement('form');
    form.method = 'GET';
    
    if (format === 'csv') {
        form.action = '/export/csv/';
    } else if (format === 'excel') {
        form.action = '/export/excel/';
    }
    
    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);
}

/**
 * Delete Confirmation
 */
function confirmDelete(itemName) {
    return confirm(`Are you sure you want to delete this application?\n\n${itemName}`);
}

/**
 * Quick Add Application Modal Handler
 */
function handleQuickAdd() {
    const form = document.getElementById('quickAddForm');
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const csrfToken = getCsrfToken();
        
        fetch('/api/quick-add/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert('Application added successfully!', 'success');
                this.reset();
                
                // Close modal
                if (typeof bootstrap !== 'undefined') {
                    const modal = bootstrap.Modal.getInstance(document.getElementById('quickAddModal'));
                    if (modal) modal.hide();
                }
                
                // Reload page after brief delay
                setTimeout(() => location.reload(), 1000);
            } else {
                showAlert('Error: ' + (data.message || 'Failed to add application'), 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('An error occurred. Please try again.', 'danger');
        });
    });
}

/**
 * Initialize on page load
 */
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        handleQuickAdd();
        highlightFollowupDueRows();
    });
} else {
    handleQuickAdd();
    highlightFollowupDueRows();
}

/**
 * Utility: Multiply filter for templates
 */
window.multiply = function(a, b) {
    return a * b;
};

/**
 * Utility: Divide filter for templates
 */
window.divide = function(a, b) {
    return b !== 0 ? a / b : 0;
};

// Add template filters for Django
// Note: These should be defined in Django templates using custom filters
