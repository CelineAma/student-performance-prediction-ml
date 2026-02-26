"""
FastAPI inference service for student academic performance prediction.

This service:
- Loads a trained Random Forest pipeline (.joblib)
- Provides a POST /predict endpoint
- Accepts a single student record as JSON
- Applies preprocessing and generates prediction
- Returns predicted class and probability

Academic deployment note:
- No model training here; inference only.
- Uses the best-performing model (Random Forest) from training artifacts.
"""

import os
import logging
from typing import Any, Dict

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Paths
MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "artifacts",
    "random_forest",
    "random_forest_pipeline.joblib",
)

# Initialize FastAPI app
app = FastAPI(
    title="Student Performance Prediction API",
    description="Academic ML inference service for predicting student academic performance risk.",
    version="1.0.0",
)

# Pydantic models for request/response
class StudentRecord(BaseModel):
    """Schema for a single student record."""
    institution_type: str | None = Field(None, example="Federal")
    faculty: str | None = Field(None, example="Engineering")
    department: str | None = Field(None, example="Computer Science")
    level: int | None = Field(None, ge=100, le=500, example=200)
    entry_mode: str | None = Field(None, example="UTME")
    age: int | None = Field(None, ge=15, le=65, example=20)
    sex: str | None = Field(None, example="Male")
    state_of_origin: str | None = Field(None, example="Lagos")
    residency_status: str | None = Field(None, example="OnCampus")
    socioeconomic_band: str | None = Field(None, example="Middle")
    utme_score: int | None = Field(None, ge=0, le=400, example=250)
    post_utme_score: float | None = Field(None, ge=0, le=100, example=65.5)
    entry_qualification: str | None = Field(None, example="SSCE")
    prev_semester_gpa: float | None = Field(None, ge=0, le=5, example=3.2)
    cumulative_cgpa: float | None = Field(None, ge=0, le=5, example=3.1)
    carryover_courses_count: int | None = Field(None, ge=0, example=1)
    failed_courses_prev_semester: int | None = Field(None, ge=0, example=2)
    core_courses_failed_total: int | None = Field(None, ge=0, example=1)
    course_load_units: int | None = Field(None, ge=0, example=18)
    continuous_assessment_avg: float | None = Field(None, ge=0, le=40, example=22.5)
    attendance_rate: float | None = Field(None, ge=0, le=1, example=0.85)
    library_visits_per_month: int | None = Field(None, ge=0, example=4)
    lms_logins_per_week: int | None = Field(None, ge=0, example=6)
    assignment_submission_rate: float | None = Field(None, ge=0, le=1, example=0.9)
    late_registration_flag: int | None = Field(None, ge=0, le=1, example=0)
    financial_clearance_delay_days: int | None = Field(None, ge=0, example=0)
    disciplinary_case_flag: int | None = Field(None, ge=0, le=1, example=0)
    counselling_visits_semester: int | None = Field(None, ge=0, example=1)
    medical_leave_flag: int | None = Field(None, ge=0, le=1, example=0)

class PredictionRequest(BaseModel):
    """Request wrapper containing a single student record."""
    student: StudentRecord

class PredictionResponse(BaseModel):
    """Response containing prediction and probability."""
    prediction: int = Field(..., description="Predicted class (0=Not at risk, 1=At risk)")
    probability: float = Field(..., description="Probability of being at risk (class 1)")

# Global model variable
model: Any = None


def load_model() -> None:
    """Load the trained Random Forest pipeline from disk."""
    global model
    try:
        model = joblib.load(MODEL_PATH)
        logger.info(f"Model loaded successfully from {MODEL_PATH}")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise RuntimeError("Model loading failed")


@app.on_event("startup")
def startup_event() -> None:
    """Load model on application startup."""
    load_model()


def preprocess_input(student: Dict[str, Any]) -> pd.DataFrame:
    """
    Preprocess student data for model inference.
    
    - Convert to DataFrame (single row)
    - Add missing required fields with default values
    - Ensure all expected columns are present
    """
    # Add missing required fields with default values
    processed_student = student.copy()
    
    # Required fields that model expects but frontend doesn't provide
    processed_student['student_id_hash'] = 0  # Default hash
    processed_student['missing_count'] = 0  # Default missing count
    
    # Default values for commonly empty fields
    if 'utme_score' not in processed_student or processed_student['utme_score'] is None:
        processed_student['utme_score'] = 200  # Average UTME score
    
    if 'post_utme_score' not in processed_student or processed_student['post_utme_score'] is None:
        processed_student['post_utme_score'] = 50.0  # Average Post-UTME score
    
    # Default values for other potentially missing fields
    defaults = {
        'institution_type': 'Federal',
        'faculty': 'Engineering',
        'department': 'Computer Science',
        'level': 200,
        'entry_mode': 'UTME',
        'sex': 'Male',
        'state_of_origin': 'Lagos',
        'residency_status': 'OnCampus',
        'socioeconomic_band': 'Middle',
        'entry_qualification': 'SSCE',
        'prev_semester_gpa': 3.0,
        'cumulative_cgpa': 3.0,
        'carryover_courses_count': 0,
        'failed_courses_prev_semester': 0,
        'core_courses_failed_total': 0,
        'course_load_units': 18,
        'continuous_assessment_avg': 20.0,
        'attendance_rate': 0.8,
        'library_visits_per_month': 4,
        'lms_logins_per_week': 6,
        'assignment_submission_rate': 0.9,
        'late_registration_flag': 0,
        'financial_clearance_delay_days': 0,
        'disciplinary_case_flag': 0,
        'counselling_visits_semester': 1,
        'medical_leave_flag': 0
    }
    
    # Apply defaults for missing fields
    for field, default_value in defaults.items():
        if field not in processed_student or processed_student[field] is None:
            processed_student[field] = default_value
    
    # Convert to DataFrame (single row)
    df = pd.DataFrame([processed_student])
    logger.info(f"Input DataFrame shape: {df.shape}")
    logger.info(f"Columns: {list(df.columns)}")
    return df


@app.get("/")
def read_root() -> Dict[str, str]:
    """Root endpoint for health check."""
    return {"service": "Student Performance Prediction API", "status": "running"}


@app.get("/health")
def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "model_loaded": model is not None}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    """
    Predict academic performance risk for a single student.

    - Accepts a single student record as JSON
    - Applies preprocessing and generates prediction
    - Returns predicted class and probability

    Example request:
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
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        # Convert Pydantic model to dict
        student_dict = request.student.model_dump(exclude_unset=True)
        logger.info(f"Received prediction request for student: {student_dict}")

        # Preprocess input
        df = preprocess_input(student_dict)

        # Generate prediction
        prediction = model.predict(df)[0]
        probabilities = model.predict_proba(df)[0]

        # For binary classification, get probability of positive class (at risk)
        prob_at_risk = float(probabilities[1])

        response = PredictionResponse(
            prediction=int(prediction),
            probability=prob_at_risk,
        )
        logger.info(f"Prediction result: {response}")
        return response

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
