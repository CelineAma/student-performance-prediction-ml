# System Integration Guide – Student Performance Prediction

## System Architecture Flow

```
Frontend (HTML/CSS/JS) → Node.js API → Python ML Service → Response
       ↓                    ↓              ↓
   Browser          JWT Auth      Model Inference
```

### 1. Frontend → Node.js API
- **Endpoint:** `POST /api/auth/login` and `POST /api/predict`
- **Authentication:** JWT token stored in localStorage
- **Data format:** JSON with `student` object
- **Validation:** Client-side + server-side (express-validator)

### 2. Node.js API → Python ML Service
- **Endpoint:** `POST http://localhost:8000/predict`
- **Authentication:** None (internal service)
- **Data format:** Same JSON structure forwarded
- **Rate limiting:** 30 requests/IP per 15 minutes

### 3. Python ML Service → Response
- **Model:** Random Forest pipeline (.joblib)
- **Processing:** Preprocessing → SMOTE → Prediction
- **Response:** `{prediction: 0|1, probability: 0.0-1.0}`

## Common Errors and Fixes

### Frontend Errors
| Error | Cause | Fix |
|--------|--------|------|
| "Please login first" | No JWT token | Login again or check localStorage |
| "Network error" | Backend down | Check Node.js API is running on port 3000 |
| "Rate limit exceeded" | Too many requests | Wait 15 minutes or use different IP |
| "Session expired" | JWT token expired | Login again to refresh token |

### Node.js API Errors
| Error | Cause | Fix |
|--------|--------|------|
| "Validation failed" | Invalid input data | Check required fields and data types |
| "ML service error" | Python service down | Start FastAPI service on port 8000 |
| "Invalid credentials" | Wrong username/password | Use admin/admin123 for demo |
| "Internal server error" | Unexpected error | Check server logs |

### Python ML Service Errors
| Error | Cause | Fix |
|--------|--------|------|
| "Model loading failed" | Missing .joblib file | Ensure artifacts exist in correct path |
| "Prediction failed" | Invalid input shape | Check data preprocessing pipeline |
| "503 Service Unavailable" | Model not loaded | Restart FastAPI service |

## Testing the System

### 1. Using Postman

#### Login Test
```bash
POST http://localhost:3000/api/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

Response:
```json
{"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
```

#### Prediction Test
```bash
POST http://localhost:3000/api/predict
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>

{
  "student": {
    "cumulative_cgpa": 3.2,
    "failed_courses_prev_semester": 2,
    "carryover_courses_count": 1,
    "attendance_rate": 0.65,
    "continuous_assessment_avg": 22.5,
    "prev_semester_gpa": 2.9,
    "age": 21,
    "faculty": "Engineering",
    "institution_type": "Federal"
  }
}
```

Response:
```json
{
  "prediction": 1,
  "probability": 0.78
}
```

### 2. Using Browser

#### Step 1: Start Services
```bash
# Terminal 1: Start Python ML Service
cd backend/python
pip install -r requirements_fastapi.txt
python inference.py

# Terminal 2: Start Node.js API
cd backend/nodejs
npm install
npm run dev

# Terminal 3: Serve Frontend (optional)
cd frontend
python -m http.server 8080
# or open index.html directly
```

#### Step 2: Test in Browser
1. Open `frontend/index.html`
2. Login with: username=`admin`, password=`admin123`
3. Fill form with sample data
4. Click "Predict Risk"
5. View results

### 3. Using curl (Command Line)

#### Complete Flow Test
```bash
# 1. Login
TOKEN=$(curl -s -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | \
  jq -r '.token')

# 2. Predict
curl -X POST http://localhost:3000/api/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "student": {
      "cumulative_cgpa": 3.2,
      "failed_courses_prev_semester": 2,
      "carryover_courses_count": 1,
      "attendance_rate": 0.65,
      "continuous_assessment_avg": 22.5,
      "prev_semester_gpa": 2.9,
      "age": 21,
      "faculty": "Engineering",
      "institution_type": "Federal"
    }
  }'
```

## System Verification Checklist

### Pre-deployment Checks
- [ ] Python ML service starts on port 8000
- [ ] Model loads without errors (`artifacts/random_forest/random_forest_pipeline.joblib`)
- [ ] Node.js API starts on port 3000
- [ ] Environment variables set (`JWT_SECRET`, `PYTHON_ML_SERVICE_URL`)
- [ ] Frontend loads in browser
- [ ] Login works with demo credentials
- [ ] Prediction form validates input
- [ ] Prediction returns results
- [ ] Rate limiting active (test with >30 requests)

### Runtime Monitoring
- **Python logs:** Check model loading and prediction errors
- **Node.js logs:** Check authentication, validation, and ML service calls
- **Browser console:** Check frontend JavaScript errors
- **Network tab:** Verify API calls and responses

## Troubleshooting Guide

### Service Won't Start
1. **Python:** Check `requirements_fastapi.txt` installation
2. **Node.js:** Run `npm install` and check `package.json`
3. **Ports:** Ensure 3000 and 8000 are available

### Authentication Issues
1. **JWT Secret:** Verify `JWT_SECRET` is set in `.env`
2. **Token Storage:** Check browser localStorage
3. **Token Expiry:** Default 1 hour, restart after expiry

### Prediction Failures
1. **Model Path:** Verify `.joblib` file exists
2. **Data Format:** Check JSON structure matches schema
3. **Preprocessing:** Ensure all categorical values are valid

### Performance Issues
1. **Rate Limiting:** Adjust limits in `rateLimit.ts`
2. **Model Loading:** Consider model size and memory
3. **Network:** Check latency between services

## Production Deployment Notes

### Security
- Change default JWT secret
- Use HTTPS in production
- Implement proper user authentication
- Add input sanitization

### Scaling
- Containerize services (Docker)
- Use load balancer for multiple instances
- Implement caching for frequent predictions
- Monitor resource usage

### Monitoring
- Add structured logging
- Implement health checks
- Set up alerting for failures
- Track prediction accuracy over time
