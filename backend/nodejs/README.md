# Node.js Backend API – Student Performance Prediction

A secure, TypeScript/Express backend for an academic ML system with JWT authentication and inter-service communication to a Python ML inference service.

## Folder Structure
```
backend/nodejs/
├─ src/
│  ├─ config/
│  │  └─ index.ts          # Environment-based configuration
│  ├─ controllers/
│  │  ├─ authController.ts   # Login endpoint logic
│  │  └─ predictController.ts # Prediction endpoint logic
│  ├─ middleware/
│  │  └─ auth.ts            # JWT verification middleware
│  ├─ routes/
│  │  └─ index.ts           # API route definitions
│  ├─ services/
│  │  ├─ authService.ts      # Mock user auth + bcrypt hashing
│  │  └─ mlService.ts        # Axios client to Python ML service
│  ├─ types/
│  │  └─ index.ts            # TypeScript interfaces
│  ├─ validation/
│  │  └─ studentSchema.ts    # Joi validation schemas
│  └─ index.ts               # Express server setup
├─ .env.example                # Environment variable template
├─ package.json
└─ tsconfig.json
```

## Setup
1. Copy `.env.example` to `.env` and set `JWT_SECRET` and `PYTHON_ML_SERVICE_URL`.
2. Install dependencies: `npm install`.
3. Build: `npm run build`.
4. Start: `npm start`.

## Endpoints
- `POST /api/auth/login` – Mock login; returns JWT.
- `POST /api/predict` – Protected; accepts student data; forwards to Python ML service; returns prediction and optional risk probability.

## Security
- JWT-based authentication with environment secret.
- Passwords hashed with bcrypt.
- Token verification middleware for protected routes.

## Example Request/Response

### Login
```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```
Response:
```json
{ "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." }
```

### Predict (protected)
```bash
curl -X POST http://localhost:3000/api/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <JWT>" \
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
Response:
```json
{
  "prediction": 1,
  "probability": 0.78,
  "explanation_url": "https://example.com/explanations/abc123"
}
```

## Notes
- Replace mock user store with a real database in production.
- Ensure the Python ML service is running and reachable at `PYTHON_ML_SERVICE_URL`.
- Use environment variables for secrets; never commit `.env`.
