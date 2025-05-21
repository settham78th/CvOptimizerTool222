// Main JavaScript for CV Generator

document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(event) {
            // Get all required fields
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            // Check each required field
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                    
                    // Create error message if it doesn't exist
                    if (!field.nextElementSibling || !field.nextElementSibling.classList.contains('invalid-feedback')) {
                        const errorMessage = document.createElement('div');
                        errorMessage.classList.add('invalid-feedback');
                        errorMessage.textContent = 'This field is required.';
                        field.parentNode.insertBefore(errorMessage, field.nextElementSibling);
                    }
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            // Prevent submission if form is invalid
            if (!isValid) {
                event.preventDefault();
            }
        });
        
        // Remove validation styling on input
        const inputs = form.querySelectorAll('input, textarea');
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                if (this.value.trim()) {
                    this.classList.remove('is-invalid');
                }
            });
        });
    }
    
    // Add clear indication to users about factual information
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('focus', function() {
            const helpText = this.nextElementSibling;
            if (helpText && helpText.classList.contains('form-text')) {
                helpText.style.color = '#0d6efd';
                helpText.style.fontWeight = 'bold';
            }
        });
        
        textarea.addEventListener('blur', function() {
            const helpText = this.nextElementSibling;
            if (helpText && helpText.classList.contains('form-text')) {
                helpText.style.color = '';
                helpText.style.fontWeight = '';
            }
        });
    });
});
