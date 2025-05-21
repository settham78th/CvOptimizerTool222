// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Form elements
    const cvUploadForm = document.getElementById('cv-upload-form');
    const cvFileInput = document.getElementById('cv-file');
    const jobDescriptionInput = document.getElementById('job-description');
    const jobUrlInput = document.getElementById('job-url');
    const processButton = document.getElementById('process-button');
    const uploadSuccessAlert = document.getElementById('upload-success');
    const uploadErrorAlert = document.getElementById('upload-error');
    const errorMessageSpan = document.getElementById('error-message');
    const processingIndicator = document.getElementById('processing-indicator');
    
    // CV preview and editor elements
    const cvPreview = document.getElementById('cv-preview');
    const cvEditor = document.getElementById('cv-editor');
    const cvTextEditor = document.getElementById('cv-text-editor');
    const editCvBtn = document.getElementById('edit-cv-btn');
    const saveCvBtn = document.getElementById('save-cv-btn');
    const cancelEditBtn = document.getElementById('cancel-edit-btn');
    
    // Result elements
    const resultContainer = document.getElementById('result-container');
    const copyResultBtn = document.getElementById('copy-result-btn');
    
    // Options elements
    const optionInputs = document.querySelectorAll('input[name="optimization-option"]');
    const multiVersionsOption = document.getElementById('multi_versions');
    const marketTrendsOption = document.getElementById('market_trends');
    const rolesContainer = document.getElementById('roles-container');
    const marketTrendsContainer = document.getElementById('market-trends-container');
    const targetRolesInput = document.getElementById('target-roles');
    const jobTitleInput = document.getElementById('job-title');
    const industryInput = document.getElementById('industry');
    
    // Store CV text
    let cvText = '';
    
    // Handle CV upload form submission
    cvUploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Check if a file is selected
        if (!cvFileInput.files[0]) {
            showError('Please select a PDF file to upload.');
            return;
        }
        
        // Create FormData object
        const formData = new FormData();
        formData.append('cv_file', cvFileInput.files[0]);
        
        // Show loading state
        processButton.disabled = true;
        cvFileInput.disabled = true;
        
        // Hide previous alerts
        uploadSuccessAlert.style.display = 'none';
        uploadErrorAlert.style.display = 'none';
        
        // Send AJAX request to upload endpoint
        fetch('/upload-cv', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Store the CV text
                cvText = data.cv_text;
                
                // Display the CV text in the preview
                cvPreview.innerHTML = formatTextAsHtml(cvText);
                
                // Enable editing and processing
                editCvBtn.disabled = false;
                processButton.disabled = false;
                
                // Show success message
                uploadSuccessAlert.style.display = 'block';
            } else {
                showError(data.message || 'Error uploading CV');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showError('Failed to upload CV. Please try again.');
        })
        .finally(() => {
            // Re-enable the file input
            cvFileInput.disabled = false;
        });
    });
    
    // Process CV button click
    processButton.addEventListener('click', function() {
        // Get selected option
        const selectedOption = document.querySelector('input[name="optimization-option"]:checked').value;
        
        // Get job description and URL
        const jobDescription = jobDescriptionInput.value.trim();
        const jobUrl = jobUrlInput.value.trim();
        
        // For multi-versions option, check if roles are provided
        let roles = [];
        if (selectedOption === 'multi_versions') {
            roles = targetRolesInput.value.trim().split('\n').filter(role => role.trim() !== '');
            if (roles.length === 0) {
                showError('Please enter at least one target role.');
                return;
            }
        }
        
        // For options that require a job description, check if one is provided
        if ((selectedOption === 'optimize' || selectedOption === 'cover_letter' || selectedOption === 'feedback' || 
             selectedOption === 'ats_check' || selectedOption === 'interview_questions') 
            && !jobDescription && !jobUrl) {
            showError('Please provide a job description or URL for this option.');
            return;
        }
        
        // For market trends option, check if job title is provided
        if (selectedOption === 'market_trends' && !jobTitleInput.value.trim()) {
            showError('Please enter a job title for market trends analysis.');
            return;
        }
        
        // Prepare request data
        const requestData = {
            cv_text: cvText,
            job_description: jobDescription,
            job_url: jobUrl,
            selected_option: selectedOption,
            roles: roles,
            job_title: jobTitleInput.value.trim(),
            industry: industryInput.value.trim()
        };
        
        // Show processing indicator and disable buttons
        processingIndicator.style.display = 'block';
        processButton.disabled = true;
        editCvBtn.disabled = true;
        uploadSuccessAlert.style.display = 'none';
        uploadErrorAlert.style.display = 'none';
        
        // Clear previous results
        resultContainer.innerHTML = '<p class="text-center">Processing your request...</p>';
        
        // Send AJAX request to process endpoint
        fetch('/process-cv', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Display the result
                resultContainer.innerHTML = formatTextAsHtml(data.result);
                
                // If job description was extracted from URL, update the input
                if (data.job_description) {
                    jobDescriptionInput.value = data.job_description;
                }
                
                // Enable copy button
                copyResultBtn.disabled = false;
            } else {
                showError(data.message || 'Error processing CV');
                resultContainer.innerHTML = '<p class="text-center text-danger">Processing failed. Please try again.</p>';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showError('Failed to process CV. Please try again.');
            resultContainer.innerHTML = '<p class="text-center text-danger">Processing failed. Please try again.</p>';
        })
        .finally(() => {
            // Hide processing indicator and re-enable buttons
            processingIndicator.style.display = 'none';
            processButton.disabled = false;
            editCvBtn.disabled = false;
        });
    });
    
    // Edit CV button click
    editCvBtn.addEventListener('click', function() {
        // Set editor text and show editor
        cvTextEditor.value = cvText;
        cvPreview.style.display = 'none';
        cvEditor.style.display = 'block';
        editCvBtn.disabled = true;
    });
    
    // Save CV button click
    saveCvBtn.addEventListener('click', function() {
        // Update CV text and preview
        cvText = cvTextEditor.value;
        cvPreview.innerHTML = formatTextAsHtml(cvText);
        
        // Hide editor and show preview
        cvEditor.style.display = 'none';
        cvPreview.style.display = 'block';
        editCvBtn.disabled = false;
    });
    
    // Cancel edit button click
    cancelEditBtn.addEventListener('click', function() {
        // Hide editor without saving changes
        cvEditor.style.display = 'none';
        cvPreview.style.display = 'block';
        editCvBtn.disabled = false;
    });
    
    // Copy result button click
    copyResultBtn.addEventListener('click', function() {
        // Get the text content from the result container
        const resultText = resultContainer.innerText;
        
        // Copy to clipboard
        navigator.clipboard.writeText(resultText).then(
            function() {
                // Success - show temporary feedback
                const originalText = copyResultBtn.innerHTML;
                copyResultBtn.innerHTML = '<i class="fas fa-check me-1"></i>Copied!';
                
                setTimeout(function() {
                    copyResultBtn.innerHTML = originalText;
                }, 2000);
            },
            function(err) {
                console.error('Could not copy text: ', err);
                showError('Failed to copy text. Please try manually selecting and copying.');
            }
        );
    });
    
    // Show appropriate inputs based on selected option
    optionInputs.forEach(input => {
        input.addEventListener('change', function() {
            // Hide all option-specific containers first
            rolesContainer.style.display = 'none';
            marketTrendsContainer.style.display = 'none';
            
            // Show the relevant container based on the option
            if (this.value === 'multi_versions') {
                rolesContainer.style.display = 'block';
            } else if (this.value === 'market_trends') {
                marketTrendsContainer.style.display = 'block';
            }
        });
    });
    
    // Helper function to show error messages
    function showError(message) {
        errorMessageSpan.textContent = message;
        uploadErrorAlert.style.display = 'block';
    }
    
    // Helper function to format plain text as HTML
    function formatTextAsHtml(text) {
        if (!text) return '<p class="text-muted">No text available</p>';
        
        // Convert newlines to <br> tags and preserve spacing
        const formattedText = text
            .replace(/\n/g, '<br>')
            .replace(/\s{2,}/g, match => '&nbsp;'.repeat(match.length));
        
        return `<div class="text-break">${formattedText}</div>`;
    }
});
