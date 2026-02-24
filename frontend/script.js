// Student Performance Prediction System - Client-side JavaScript

// Configuration
const API_BASE_URL = 'http://localhost:3000/api';
let authToken = null;

// DOM Elements
const loginSection = document.getElementById('loginSection');
const predictionSection = document.getElementById('predictionSection');
const resultsSection = document.getElementById('resultsSection');
const loginForm = document.getElementById('loginForm');
const predictionForm = document.getElementById('predictionForm');
const loginError = document.getElementById('loginError');
const predictionError = document.getElementById('predictionError');

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    checkAuthStatus();
    setupEventListeners();
});

// Check if user is already authenticated
function checkAuthStatus() {
    const token = localStorage.getItem('authToken');
    if (token) {
        authToken = token;
        showPredictionSection();
    }
}

// Setup event listeners
function setupEventListeners() {
    // Login form
    loginForm.addEventListener('submit', handleLogin);
    
    // Prediction form
    predictionForm.addEventListener('submit', handlePrediction);
    
    // Buttons
    document.getElementById('logoutBtn').addEventListener('click', handleLogout);
    document.getElementById('clearBtn').addEventListener('click', clearForm);
    document.getElementById('newPredictionBtn').addEventListener('click', newPrediction);
}

// Handle login
async function handleLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    if (!username || !password) {
        showError(loginError, 'Please enter both username and password');
        return;
    }
    
    showLoading(e.target);
    
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });
        
        const data = await response.json();
        
        if (response.ok) {
            authToken = data.token;
            localStorage.setItem('authToken', authToken);
            hideError(loginError);
            showPredictionSection();
            showSuccess('Login successful!');
        } else {
            showError(loginError, data.error || 'Login failed');
        }
    } catch (error) {
        console.error('Login error:', error);
        showError(loginError, 'Network error. Please try again.');
    } finally {
        hideLoading(e.target);
    }
}

// Handle prediction
async function handlePrediction(e) {
    e.preventDefault();
    
    if (!authToken) {
        showError(predictionError, 'Please login first');
        return;
    }
    
    // Collect form data
    const formData = new FormData(predictionForm);
    const studentData = {};
    
    // Convert FormData to object and filter empty values
    for (let [key, value] of formData.entries()) {
        if (value.trim() !== '') {
            // Convert numeric strings to numbers
            if (['cumulative_cgpa', 'prev_semester_gpa', 'utme_score', 'post_utme_score', 
                'continuous_assessment_avg', 'attendance_rate', 'carryover_courses_count',
                'failed_courses_prev_semester', 'core_courses_failed_total', 'course_load_units',
                'age', 'library_visits_per_month', 'lms_logins_per_week',
                'assignment_submission_rate', 'financial_clearance_delay_days',
                'counselling_visits_semester'].includes(key)) {
                
                // Handle boolean/integer fields
                if (['late_registration_flag', 'disciplinary_case_flag', 'medical_leave_flag'].includes(key)) {
                    studentData[key] = parseInt(value);
                } else {
                    studentData[key] = parseFloat(value);
                }
            } else {
                studentData[key] = value;
            }
        }
    }
    
    // Validate required fields
    if (!studentData.cumulative_cgpa) {
        showError(predictionError, 'Cumulative CGPA is required');
        return;
    }
    
    showLoading(e.target);
    
    try {
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`,
            },
            body: JSON.stringify({ student: studentData }),
        });
        
        const data = await response.json();
        
        if (response.ok) {
            hideError(predictionError);
            showResults(data);
        } else {
            if (response.status === 429) {
                showError(predictionError, 'Rate limit exceeded. Please try again later.');
            } else if (response.status === 401) {
                showError(predictionError, 'Session expired. Please login again.');
                handleLogout();
            } else {
                showError(predictionError, data.error || 'Prediction failed');
            }
        }
    } catch (error) {
        console.error('Prediction error:', error);
        showError(predictionError, 'Network error. Please try again.');
    } finally {
        hideLoading(e.target);
    }
}

// Show prediction results
function showResults(data) {
    const resultContainer = document.getElementById('predictionResult');
    const isAtRisk = data.prediction === 1;
    const probability = (data.probability * 100).toFixed(1);
    
    resultContainer.innerHTML = `
        <div class="result-container ${isAtRisk ? 'result-risk-high' : 'result-risk-low'}">
            <div class="result-title">
                ${isAtRisk ? '⚠️ At Risk' : '✅ Not at Risk'}
            </div>
            <div class="result-probability">
                Risk Probability: ${probability}%
            </div>
            <div class="result-description">
                ${isAtRisk 
                    ? 'The student shows indicators of academic risk. Consider academic support interventions.'
                    : 'The student appears to be on track academically. Continue monitoring.'
                }
            </div>
        </div>
    `;
    
    predictionSection.style.display = 'none';
    resultsSection.style.display = 'block';
}

// Handle logout
function handleLogout() {
    localStorage.removeItem('authToken');
    authToken = null;
    showLoginSection();
    showSuccess('Logged out successfully');
}

// New prediction
function newPrediction() {
    resultsSection.style.display = 'none';
    predictionSection.style.display = 'block';
    clearForm();
}

// Clear form
function clearForm() {
    predictionForm.reset();
    hideError(predictionError);
}

// Show/hide sections
function showLoginSection() {
    loginSection.style.display = 'block';
    predictionSection.style.display = 'none';
    resultsSection.style.display = 'none';
}

function showPredictionSection() {
    loginSection.style.display = 'none';
    predictionSection.style.display = 'block';
    resultsSection.style.display = 'none';
}

// Error handling
function showError(element, message) {
    element.textContent = message;
    element.classList.add('show');
    setTimeout(() => {
        element.classList.remove('show');
    }, 5000);
}

function hideError(element) {
    element.classList.remove('show');
}

// Loading states
function showLoading(button) {
    button.disabled = true;
    const originalText = button.textContent;
    button.innerHTML = `<span class="loading"></span>Processing...`;
    button.dataset.originalText = originalText;
}

function hideLoading(button) {
    button.disabled = false;
    if (button.dataset.originalText) {
        button.textContent = button.dataset.originalText;
        delete button.dataset.originalText;
    }
}

// Success message
function showSuccess(message) {
    // Create a temporary success message
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.textContent = message;
    successDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: var(--success-color);
        color: white;
        padding: 12px 20px;
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(successDiv);
    
    setTimeout(() => {
        successDiv.remove();
    }, 3000);
}

// Add slide-in animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .success-message {
        animation: slideIn 0.3s ease;
    }
`;
document.head.appendChild(style);

// Client-side validation helpers
function validateField(field, value, rules) {
    for (const rule of rules) {
        if (rule.required && (!value || value.trim() === '')) {
            return `${field} is required`;
        }
        
        if (rule.min && parseFloat(value) < rule.min) {
            return `${field} must be at least ${rule.min}`;
        }
        
        if (rule.max && parseFloat(value) > rule.max) {
            return `${field} must be at most ${rule.max}`;
        }
        
        if (rule.pattern && !rule.pattern.test(value)) {
            return `${field} format is invalid`;
        }
    }
    
    return null;
}

// Add real-time validation to key fields
document.getElementById('cumulative_cgpa').addEventListener('blur', function() {
    const error = validateField('CGPA', this.value, [
        { required: true },
        { min: 0 },
        { max: 5 }
    ]);
    
    if (error) {
        this.style.borderColor = 'var(--danger-color)';
        showError(predictionError, error);
    } else {
        this.style.borderColor = '#ddd';
        hideError(predictionError);
    }
});

document.getElementById('attendance_rate').addEventListener('blur', function() {
    const error = validateField('Attendance Rate', this.value, [
        { required: false },
        { min: 0 },
        { max: 1 }
    ]);
    
    if (error) {
        this.style.borderColor = 'var(--danger-color)';
        showError(predictionError, error);
    } else {
        this.style.borderColor = '#ddd';
        hideError(predictionError);
    }
});

// Handle network errors gracefully
window.addEventListener('online', () => {
    showSuccess('Connection restored');
});

window.addEventListener('offline', () => {
    showError(predictionError, 'You are offline. Please check your connection.');
});

// Auto-refresh token before expiry (optional enhancement)
function refreshToken() {
    // Implementation for token refresh if needed
    console.log('Token refresh would happen here if implemented');
}

// Periodic session check
setInterval(() => {
    if (authToken) {
        // Optionally validate token with server
        console.log('Session active');
    }
}, 60000); // Check every minute
