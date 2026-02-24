# FastAPI Inference Service – Student Performance Prediction

A lightweight FastAPI service for serving predictions from the trained Random Forest model. This service is designed for academic deployment and provides only inference (no training).

## Quick Start

```bash
# Install dependencies
pip install -r requirements_fastapi.txt

# Run the service
python inference.py
```

The service will start on `http://0.0.0.0:8000`.

## Endpoints

### GET /
Root/health check.

### GET /health
Health check with model loading status.

### POST /predict
Accepts a single student record and returns prediction.

## Example Request

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
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

## Example Response

```json
{
  "prediction": 1,
  "probability": 0.78
}
```

- `prediction`: 0 = Not at risk, 1 = At risk
- `probability`: Probability of being at risk (class 1)

## Architecture

- **Model**: Loads `random_forest_pipeline.joblib` (best-performing model)
- **Preprocessing**: Pipeline handles imputation, scaling, and one-hot encoding internally
- **Validation**: Pydantic models enforce input schema
- **Error handling**: Structured HTTP errors with logging

## Academic Deployment Notes

- Inference-only service; no training endpoints exposed
- Uses Random Forest (best macro F1 on test set)
- Logs predictions for auditability
- Suitable for containerized deployment in academic environments
