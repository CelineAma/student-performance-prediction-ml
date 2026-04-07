// Student Performance Prediction System - Client-side JavaScript

const API_BASE_URL = 'http://localhost:3000/api';
let authToken = null;

const loginSection = document.getElementById('loginSection');
const predictionSection = document.getElementById('predictionSection');
const resultsSection = document.getElementById('resultsSection');
const loginForm = document.getElementById('loginForm');
const predictionForm = document.getElementById('predictionForm');
const loginError = document.getElementById('loginError');
const predictionError = document.getElementById('predictionError');

document.addEventListener('DOMContentLoaded', () => {
    checkAuthStatus();
    setupEventListeners();
    setupStepProgress();
});

function setupStepProgress() {
    const stepItems = document.querySelectorAll('.step-item');
    const progressFill = document.getElementById('stepProgressFill');
    
    if (!stepItems.length || !progressFill) return;
    
const observerOptions = {
        root: null,
        rootMargin: '-20% 0px -60% 0px',
        threshold: 0
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const targetId = entry.target.id;
                updateActiveStep(targetId);
            }
        });
    }, observerOptions);
    
const fieldsets = document.querySelectorAll('.fieldset');
    fieldsets.forEach(fieldset => {
        observer.observe(fieldset);
    });
    
stepItems.forEach(item => {
        item.addEventListener('click', () => {
            const targetId = item.dataset.target;
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
}

function updateActiveStep(targetId) {
    const stepItems = document.querySelectorAll('.step-item');
    const progressFill = document.getElementById('stepProgressFill');
    
    if (!stepItems.length || !progressFill) return;
    
let activeStepIndex = -1;
    stepItems.forEach((item, index) => {
        if (item.dataset.target === targetId) {
            activeStepIndex = index;
        }
    });
    
    if (activeStepIndex === -1) return;
    
stepItems.forEach((item, index) => {
        item.classList.remove('active', 'completed');
        
        if (index < activeStepIndex) {
            item.classList.add('completed');
        } else if (index === activeStepIndex) {
            item.classList.add('active');
        }
    });
    
const progressPercentage = ((activeStepIndex + 1) / stepItems.length) * 100;
    progressFill.style.width = `${progressPercentage}%`;
}

function checkAuthStatus() {
    const token = localStorage.getItem('authToken');
    if (token) {
        authToken = token;
        showPredictionSection();
    }
}

function setupEventListeners() {
loginForm.addEventListener('submit', handleLogin);
    
predictionForm.addEventListener('submit', handlePrediction);
    
document.getElementById('logoutBtn').addEventListener('click', handleLogout);
    document.getElementById('clearBtn').addEventListener('click', clearForm);
    document.getElementById('newPredictionBtn').addEventListener('click', newPrediction);
}

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

async function handlePrediction(e) {
    e.preventDefault();
    
    if (!authToken) {
        showError(predictionError, 'Please login first');
        return;
    }
    
const formData = new FormData(predictionForm);
    const studentData = {};
    
for (let [key, value] of formData.entries()) {
        if (value.trim() !== '') {
if (['cumulative_cgpa', 'prev_semester_gpa', 'utme_score', 'post_utme_score', 
                'continuous_assessment_avg', 'attendance_rate', 'carryover_courses_count',
                'failed_courses_prev_semester', 'core_courses_failed_total', 'course_load_units',
                'age', 'library_visits_per_month', 'lms_logins_per_week',
                'assignment_submission_rate', 'financial_clearance_delay_days',
                'counselling_visits_semester'].includes(key)) {
                
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
            } else if (response.status === 403) {
                showError(predictionError, 'Invalid or expired token. Please login again.');
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

function showResults(data) {
    const resultContainer = document.getElementById('predictionResult');
    const isAtRisk = data.prediction === 1;
    const probability = (data.probability * 100).toFixed(1);
    
    resultContainer.innerHTML = `
        <div class="result-container ${isAtRisk ? 'result-risk-high' : 'result-risk-low'}">
            <!-- Risk Badge -->
            <div class="risk-badge ${isAtRisk ? 'risk-high' : 'risk-low'}">
                ${isAtRisk ? '🔴 High Risk' : '🟢 Low Risk'}
            </div>
            
            <!-- Risk Meter -->
            <div class="risk-meter-container">
                <div class="risk-meter-label">Risk Level</div>
                <div class="risk-meter-bar">
                    <div class="risk-meter-fill ${isAtRisk ? 'risk-fill-high' : 'risk-fill-low'}" 
                         style="width: ${probability}%">
                    </div>
                </div>
                <div class="risk-meter-percentage">${probability}%</div>
            </div>
            
            <!-- Result Title -->
            <div class="result-title">
                ${isAtRisk ? '⚠️ At Risk' : '✅ Not at Risk'}
            </div>
            
            <!-- Result Description -->
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

function handleLogout() {
    localStorage.removeItem('authToken');
    authToken = null;
    showLoginSection();
    showSuccess('Logged out successfully');
}

function newPrediction() {
    resultsSection.style.display = 'none';
    predictionSection.style.display = 'block';
    clearForm();
}

function clearForm() {
    predictionForm.reset();
    hideError(predictionError);
}

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

function showSuccess(message) {
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

window.addEventListener('online', () => {
    showSuccess('Connection restored');
});

window.addEventListener('offline', () => {
    showError(predictionError, 'You are offline. Please check your connection.');
});

function refreshToken() {
    // Implementation for token refresh if needed
    console.log('Token refresh would happen here if implemented');
}

setInterval(() => {
    if (authToken) {
console.log('Session active');
    }
}, 60000); // Check every minute
