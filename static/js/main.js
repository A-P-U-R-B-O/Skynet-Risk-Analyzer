// Skynet Risk Analyzer - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    console.log('Skynet Risk Analyzer initialized');
    
    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor. addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this. getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Form validation
    const analyzeForm = document.getElementById('analyzeForm');
    if (analyzeForm) {
        analyzeForm.addEventListener('submit', function(e) {
            const nameInput = document.getElementById('name');
            if (! nameInput.value.trim()) {
                e.preventDefault();
                alert('Please enter an AI system name');
                nameInput.focus();
            }
        });
    }
    
    // Add tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Range slider value updater
function updateValue(name, value) {
    const displayElement = document.getElementById(name + 'Value');
    if (displayElement) {
        displayElement.textContent = value;
        
        // Color code based on risk
        const numValue = parseInt(value);
        if (numValue >= 80) {
            displayElement.className = 'risk-critical';
        } else if (numValue >= 60) {
            displayElement.className = 'risk-high';
        } else if (numValue >= 40) {
            displayElement.className = 'risk-moderate';
        } else if (numValue >= 20) {
            displayElement.className = 'risk-low';
        } else {
            displayElement.className = 'risk-minimal';
        }
    }
}
