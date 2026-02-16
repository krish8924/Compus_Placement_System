// Main JavaScript for Campus Placement System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Check for notifications (if user is logged in)
    checkNotifications();
    
    // Add confirm dialog to delete buttons
    setupDeleteConfirmations();
    
    // Add form validation
    setupFormValidation();
    
    // Setup file upload preview
    setupFileUploadPreview();
});

// Function to check for notifications
function checkNotifications() {
    const notificationCount = document.getElementById('notification-count');
    const notificationList = document.getElementById('notification-list');
    
    if (!notificationCount || !notificationList) {
        return; // User might not be logged in
    }
    
    // Check for unread notifications every 60 seconds
    fetchNotifications();
    setInterval(fetchNotifications, 60000);
    
    function fetchNotifications() {
        // This would normally be an AJAX call to the server
        // For now, we'll use a placeholder that will be replaced with actual AJAX
        
        // Sample code for when backend API is ready:
        /*
        fetch('/api/notifications/unread/')
            .then(response => response.json())
            .then(data => {
                updateNotificationUI(data);
            })
            .catch(error => console.error('Error fetching notifications:', error));
        */
        
        // For now, we'll simply update the UI with a placeholder
        // This would be replaced by actual notification data from the backend
        const unreadCount = parseInt(notificationCount.textContent) || 0;
        if (unreadCount > 0) {
            notificationCount.textContent = unreadCount;
            notificationCount.style.display = 'inline-block';
        } else {
            notificationCount.style.display = 'none';
        }
    }
}

// Function to setup delete confirmations
function setupDeleteConfirmations() {
    const deleteButtons = document.querySelectorAll('.btn-delete');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
}

// Function to setup form validation
function setupFormValidation() {
    // Get all forms that need validation
    const forms = document.querySelectorAll('.needs-validation');
    
    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
}

// Function to setup file upload preview
function setupFileUploadPreview() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            const previewElement = document.getElementById(`${this.id}-preview`);
            if (!previewElement) return;
            
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    previewElement.innerHTML = '';
                    
                    if (input.accept.includes('image')) {
                        // Show image preview
                        const img = document.createElement('img');
                        img.src = e.target.result;
                        img.className = 'img-thumbnail mt-2';
                        img.style.maxHeight = '200px';
                        previewElement.appendChild(img);
                    } else {
                        // Show file name
                        const fileInfo = document.createElement('div');
                        fileInfo.className = 'alert alert-info mt-2';
                        fileInfo.innerHTML = `<i class="fas fa-file me-2"></i> ${input.files[0].name}`;
                        previewElement.appendChild(fileInfo);
                    }
                }
                
                reader.readAsDataURL(this.files[0]);
            }
        });
    });
}

// Function to toggle password visibility
function togglePasswordVisibility(inputId) {
    const passwordInput = document.getElementById(inputId);
    const icon = document.querySelector(`[data-password-toggle="${inputId}"] i`);
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

// Function to show loading spinner during form submission
function showLoadingSpinner() {
    const spinnerOverlay = document.createElement('div');
    spinnerOverlay.className = 'spinner-overlay';
    spinnerOverlay.innerHTML = `
        <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    `;
    
    document.body.appendChild(spinnerOverlay);
    
    return spinnerOverlay;
}

// Function to remove loading spinner
function hideLoadingSpinner(spinner) {
    if (spinner && spinner.parentNode) {
        spinner.parentNode.removeChild(spinner);
    }
}

// Helper function to format date
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

// Helper function to format datetime
function formatDateTime(dateTimeString) {
    const options = { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(dateTimeString).toLocaleString(undefined, options);
}

// Helper function for string formatting (to avoid null or undefined values)
function formatString(str, defaultValue = '') {
    return str || defaultValue;
}
