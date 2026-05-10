# Test Data for Student Performance Prediction API

## Authentication

### Login Request (Postman)
```json
{
  "username": "admin",
  "password": "password123"
}
```

### Login Response
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

## Prediction Test Data

### Scenario 1: High-Performing Student (Low Risk)
**Expected**: Prediction 0 (Not at risk)

**Postman Request Body**:
```json
{
  "student": {
    "institution_type": "Federal",
    "faculty": "Engineering",
    "department": "Computer Engineering",
    "level": 300,
    "entry_mode": "UTME",
    "age": 20,
    "sex": "Male",
    "state_of_origin": "Lagos",
    "residency_status": "OnCampus",
    "socioeconomic_band": "High",
    "utme_score": 350,
    "post_utme_score": 85,
    "entry_qualification": "SSCE",
    "prev_semester_gpa": 4.2,
    "cumulative_cgpa": 4.1,
    "carryover_courses_count": 0,
    "failed_courses_prev_semester": 0,
    "core_courses_failed_total": 0,
    "course_load_units": 24,
    "continuous_assessment_avg": 35,
    "attendance_rate": 0.95,
    "library_visits_per_month": 15,
    "lms_logins_per_week": 12,
    "assignment_submission_rate": 1.0,
    "late_registration_flag": 0,
    "financial_clearance_delay_days": 0,
    "disciplinary_case_flag": 0,
    "counselling_visits_semester": 0,
    "medical_leave_flag": 0
  }
}
```

### Scenario 2: At-Risk Student (High Risk)
**Expected**: Prediction 1 (At risk)

**Postman Request Body**:
```json
{
  "student": {
    "institution_type": "State",
    "faculty": "Arts",
    "department": "English Language",
    "level": 200,
    "entry_mode": "DirectEntry",
    "age": 25,
    "sex": "Female",
    "state_of_origin": "Kano",
    "residency_status": "OffCampus",
    "socioeconomic_band": "Low",
    "utme_score": 180,
    "post_utme_score": 45,
    "entry_qualification": "ND",
    "prev_semester_gpa": 1.8,
    "cumulative_cgpa": 2.1,
    "carryover_courses_count": 4,
    "failed_courses_prev_semester": 3,
    "core_courses_failed_total": 5,
    "course_load_units": 18,
    "continuous_assessment_avg": 15,
    "attendance_rate": 0.6,
    "library_visits_per_month": 2,
    "lms_logins_per_week": 3,
    "assignment_submission_rate": 0.7,
    "late_registration_flag": 1,
    "financial_clearance_delay_days": 30,
    "disciplinary_case_flag": 1,
    "counselling_visits_semester": 4,
    "medical_leave_flag": 0
  }
}
```

### Scenario 3: Average Student (Medium Risk)
**Expected**: Could be either 0 or 1 depending on model

**Postman Request Body**:
```json
{
  "student": {
    "institution_type": "Private",
    "faculty": "Sciences",
    "department": "Mathematics",
    "level": 100,
    "entry_mode": "UTME",
    "age": 18,
    "sex": "Male",
    "state_of_origin": "Abuja",
    "residency_status": "OnCampus",
    "socioeconomic_band": "Middle",
    "utme_score": 250,
    "post_utme_score": 65,
    "entry_qualification": "SSCE",
    "prev_semester_gpa": 3.0,
    "cumulative_cgpa": 3.0,
    "carryover_courses_count": 1,
    "failed_courses_prev_semester": 1,
    "core_courses_failed_total": 1,
    "course_load_units": 21,
    "continuous_assessment_avg": 25,
    "attendance_rate": 0.8,
    "library_visits_per_month": 8,
    "lms_logins_per_week": 6,
    "assignment_submission_rate": 0.85,
    "late_registration_flag": 0,
    "financial_clearance_delay_days": 7,
    "disciplinary_case_flag": 0,
    "counselling_visits_semester": 1,
    "medical_leave_flag": 0
  }
}
```

### Scenario 4: Minimal Data (Edge Case)
**Expected**: Should work with optional fields

**Postman Request Body**:
```json
{
  "student": {
    "age": 19,
    "sex": "Female",
    "prev_semester_gpa": 2.5,
    "cumulative_cgpa": 2.8
  }
}
```

---

## Browser Testing Data

### HTML Form for Browser Testing
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Performance Prediction Test</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, select { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        button { background-color: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background-color: #0056b3; }
        .result { margin-top: 20px; padding: 15px; border-radius: 4px; }
        .success { background-color: #d4edda; color: #155724; }
        .error { background-color: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <h1>Student Performance Prediction Test</h1>
    
    <div>
        <h3>Authentication</h3>
        <div class="form-group">
            <label>Username:</label>
            <input type="text" id="username" value="admin">
        </div>
        <div class="form-group">
            <label>Password:</label>
            <input type="password" id="password" value="password123">
        </div>
        <button onclick="login()">Login</button>
        <div id="authResult"></div>
    </div>

    <hr>

    <div>
        <h3>Prediction Test</h3>
        <div class="form-group">
            <label>Test Scenario:</label>
            <select id="testScenario" onchange="loadScenario()">
                <option value="highPerformer">High Performing Student</option>
                <option value="atRisk">At-Risk Student</option>
                <option value="average">Average Student</option>
                <option value="minimal">Minimal Data</option>
            </select>
        </div>
        <button onclick="testPrediction()">Test Prediction</button>
        <div id="predictionResult"></div>
    </div>

    <script>
        let authToken = '';

        const testScenarios = {
            highPerformer: {
                institution_type: "Federal",
                faculty: "Engineering",
                department: "Computer Engineering",
                level: 300,
                entry_mode: "UTME",
                age: 20,
                sex: "Male",
                state_of_origin: "Lagos",
                residency_status: "OnCampus",
                socioeconomic_band: "High",
                utme_score: 350,
                post_utme_score: 85,
                entry_qualification: "SSCE",
                prev_semester_gpa: 4.2,
                cumulative_cgpa: 4.1,
                carryover_courses_count: 0,
                failed_courses_prev_semester: 0,
                core_courses_failed_total: 0,
                course_load_units: 24,
                continuous_assessment_avg: 35,
                attendance_rate: 0.95,
                library_visits_per_month: 15,
                lms_logins_per_week: 12,
                assignment_submission_rate: 1.0,
                late_registration_flag: 0,
                financial_clearance_delay_days: 0,
                disciplinary_case_flag: 0,
                counselling_visits_semester: 0,
                medical_leave_flag: 0
            },
            atRisk: {
                institution_type: "State",
                faculty: "Arts",
                department: "English Language",
                level: 200,
                entry_mode: "DirectEntry",
                age: 25,
                sex: "Female",
                state_of_origin: "Kano",
                residency_status: "OffCampus",
                socioeconomic_band: "Low",
                utme_score: 180,
                post_utme_score: 45,
                entry_qualification: "ND",
                prev_semester_gpa: 1.8,
                cumulative_cgpa: 2.1,
                carryover_courses_count: 4,
                failed_courses_prev_semester: 3,
                core_courses_failed_total: 5,
                course_load_units: 18,
                continuous_assessment_avg: 15,
                attendance_rate: 0.6,
                library_visits_per_month: 2,
                lms_logins_per_week: 3,
                assignment_submission_rate: 0.7,
                late_registration_flag: 1,
                financial_clearance_delay_days: 30,
                disciplinary_case_flag: 1,
                counselling_visits_semester: 4,
                medical_leave_flag: 0
            },
            average: {
                institution_type: "Private",
                faculty: "Sciences",
                department: "Mathematics",
                level: 100,
                entry_mode: "UTME",
                age: 18,
                sex: "Male",
                state_of_origin: "Abuja",
                residency_status: "OnCampus",
                socioeconomic_band: "Middle",
                utme_score: 250,
                post_utme_score: 65,
                entry_qualification: "SSCE",
                prev_semester_gpa: 3.0,
                cumulative_cgpa: 3.0,
                carryover_courses_count: 1,
                failed_courses_prev_semester: 1,
                core_courses_failed_total: 1,
                course_load_units: 21,
                continuous_assessment_avg: 25,
                attendance_rate: 0.8,
                library_visits_per_month: 8,
                lms_logins_per_week: 6,
                assignment_submission_rate: 0.85,
                late_registration_flag: 0,
                financial_clearance_delay_days: 7,
                disciplinary_case_flag: 0,
                counselling_visits_semester: 1,
                medical_leave_flag: 0
            },
            minimal: {
                age: 19,
                sex: "Female",
                prev_semester_gpa: 2.5,
                cumulative_cgpa: 2.8
            }
        };

        async function login() {
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            try {
                const response = await fetch('/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username, password })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    authToken = data.token;
                    document.getElementById('authResult').innerHTML = 
                        `<div class="result success">Login successful! Token: ${authToken.substring(0, 20)}...</div>`;
                } else {
                    document.getElementById('authResult').innerHTML = 
                        `<div class="result error">Login failed: ${data.error}</div>`;
                }
            } catch (error) {
                document.getElementById('authResult').innerHTML = 
                    `<div class="result error">Network error: ${error.message}</div>`;
            }
        }

        async function testPrediction() {
            if (!authToken) {
                document.getElementById('predictionResult').innerHTML = 
                    '<div class="result error">Please login first!</div>';
                return;
            }

            const scenario = document.getElementById('testScenario').value;
            const studentData = testScenarios[scenario];
            
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${authToken}`
                    },
                    body: JSON.stringify({ student: studentData })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    const riskLevel = data.prediction === 1 ? 'At Risk' : 'Not at Risk';
                    const probability = data.probability ? ` (Probability: ${(data.probability * 100).toFixed(2)}%)` : '';
                    document.getElementById('predictionResult').innerHTML = 
                        `<div class="result success">
                            <strong>Prediction:</strong> ${riskLevel}${probability}<br>
                            <strong>Explanation:</strong> ${data.explanation_url || 'Not available'}
                        </div>`;
                } else {
                    document.getElementById('predictionResult').innerHTML = 
                        `<div class="result error">Prediction failed: ${data.error || 'Unknown error'}</div>`;
                }
            } catch (error) {
                document.getElementById('predictionResult').innerHTML = 
                    `<div class="result error">Network error: ${error.message}</div>`;
            }
        }

        function loadScenario() {
            // This function could be used to populate a detailed form if needed
            console.log('Scenario loaded:', document.getElementById('testScenario').value);
        }
    </script>
</body>
</html>
```

---

## Postman Collection Setup

### Environment Variables
```
base_url: http://localhost:3000
auth_token: {{auth_token}}
```

### Collection Requests

#### 1. Login
- **Method**: POST
- **URL**: `{{base_url}}/auth/login`
- **Headers**: Content-Type: application/json
- **Body**: raw JSON (see login request above)
- **Tests**: 
```javascript
if (pm.response.code === 200) {
    const response = pm.response.json();
    pm.environment.set("auth_token", response.token);
}
```

#### 2. Predict
- **Method**: POST
- **URL**: `{{base_url}}/predict`
- **Headers**: 
  - Content-Type: application/json
  - Authorization: Bearer {{auth_token}}
- **Body**: raw JSON (see prediction requests above)

---

## Error Testing Scenarios

### Invalid Authentication
```json
{
  "username": "wrong",
  "password": "wrong"
}
```

### Invalid Data Types
```json
{
  "student": {
    "age": "twenty",  // Should be number
    "sex": "Other",   // Invalid enum value
    "prev_semester_gpa": 6.0  // Above max value
  }
}
```

### Missing Required Fields
```json
{
  "student": {
    "faculty": "Engineering"
    // Missing other fields that might be required by validation
  }
}
```

### Empty Request
```json
{}
```

---

## Expected Response Formats

### Success Response
```json
{
  "prediction": 0,
  "probability": 0.15,
  "explanation_url": "/api/explanations/abc123"
}
```

### Error Response
```json
{
  "error": "Validation failed",
  "details": [
    {
      "field": "student.age",
      "message": "age must be an integer between 15 and 65",
      "value": "twenty"
    }
  ]
}
```

### Authentication Error
```json
{
  "error": "Invalid credentials"
}
```
