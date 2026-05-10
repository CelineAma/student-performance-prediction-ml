#!/usr/bin/env python3
"""
Comprehensive SHAP Explanation Generation for Academic Reporting

This script generates model explanation outputs for academic reporting (Appendix D).
It loads trained pipelines, applies preprocessing, and creates SHAP visualizations
including global summary plots, local waterfall plots, and feature importance charts.

Author: Student Performance Prediction Project
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
from sklearn.model_selection import train_test_split

from src.explainability import (
    shap_summary_plot_for_pipeline,
    shap_local_waterfall_for_pipeline,
    _pick_class_index,
    _extract_shap_for_class,
    pd_series_from_shap
)
from src.feature_engineering import BasicFeatureEngineer


def setup_matplotlib_style() -> None:
    """Configure matplotlib for academic reporting with clean styling."""
    plt.style.use('default')
    plt.rcParams.update({
        'figure.facecolor': 'white',
        'axes.facecolor': 'white',
        'axes.edgecolor': 'black',
        'axes.linewidth': 1.0,
        'axes.grid': True,
        'grid.alpha': 0.3,
        'grid.linestyle': '--',
        'font.family': 'serif',
        'font.size': 10,
        'axes.labelsize': 10,
        'axes.titlesize': 12,
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,
        'legend.fontsize': 9,
        'figure.titlesize': 14,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.1
    })


def load_pipeline_and_data(
    model_path: Path,
    data_path: Optional[Path] = None,
    target_column: str = "academic_performance"
) -> Tuple[Any, pd.DataFrame, pd.Series]:
    """Load trained pipeline and prepare data for SHAP analysis."""
    print(f"Loading pipeline from: {model_path}")
    pipeline = joblib.load(model_path)
    
    # Load or generate sample data if not provided
    if data_path and data_path.exists():
        print(f"Loading data from: {data_path}")
        df = pd.read_csv(data_path)
    else:
        print("Generating synthetic sample data...")
        df = generate_sample_data()
    
    # Apply feature engineering
    fe = BasicFeatureEngineer(add_missing_count=True)
    df_fe = fe.transform(df)
    
    if target_column not in df_fe.columns:
        raise ValueError(f"Target column '{target_column}' not found in dataset")
    
    X = df_fe.drop(columns=[target_column])
    y = df_fe[target_column]
    
    return pipeline, X, y


def generate_sample_data(n_samples: int = 1000) -> pd.DataFrame:
    """Generate synthetic student data for testing purposes."""
    np.random.seed(42)
    
    data = {
        'student_id_hash': [f'student_{i:04d}' for i in range(n_samples)],
        'institution_type': np.random.choice(['Federal', 'State', 'Private'], n_samples),
        'faculty': np.random.choice(['Engineering', 'Arts', 'Sciences', 'Social Sciences'], n_samples),
        'department': np.random.choice(['Computer Science', 'Mathematics', 'English', 'Physics'], n_samples),
        'level': np.random.choice([100, 200, 300, 400, 500], n_samples),
        'entry_mode': np.random.choice(['UTME', 'DirectEntry', 'Transfer'], n_samples),
        'age': np.random.randint(16, 35, n_samples),
        'sex': np.random.choice(['Male', 'Female'], n_samples),
        'state_of_origin': np.random.choice(['Lagos', 'Abuja', 'Kano', 'Rivers'], n_samples),
        'residency_status': np.random.choice(['OnCampus', 'OffCampus'], n_samples),
        'socioeconomic_band': np.random.choice(['Low', 'Middle', 'High'], n_samples),
        'utme_score': np.random.randint(0, 401, n_samples),
        'post_utme_score': np.random.uniform(0, 100, n_samples),
        'entry_qualification': np.random.choice(['SSCE', 'ND', 'HND', 'Alevel'], n_samples),
        'prev_semester_gpa': np.random.uniform(0, 5, n_samples),
        'cumulative_cgpa': np.random.uniform(0, 5, n_samples),
        'carryover_courses_count': np.random.randint(0, 10, n_samples),
        'failed_courses_prev_semester': np.random.randint(0, 8, n_samples),
        'core_courses_failed_total': np.random.randint(0, 15, n_samples),
        'course_load_units': np.random.randint(12, 30, n_samples),
        'continuous_assessment_avg': np.random.uniform(0, 40, n_samples),
        'attendance_rate': np.random.uniform(0, 1, n_samples),
        'library_visits_per_month': np.random.randint(0, 50, n_samples),
        'lms_logins_per_week': np.random.randint(0, 20, n_samples),
        'assignment_submission_rate': np.random.uniform(0, 1, n_samples),
        'late_registration_flag': np.random.randint(0, 2, n_samples),
        'financial_clearance_delay_days': np.random.randint(0, 60, n_samples),
        'disciplinary_case_flag': np.random.randint(0, 2, n_samples),
        'counselling_visits_semester': np.random.randint(0, 10, n_samples),
        'medical_leave_flag': np.random.randint(0, 2, n_samples),
    }
    
    # Create target variable based on key features (academic performance)
    risk_score = (
        (data['cumulative_cgpa'] < 2.5) * 2 +
        (data['failed_courses_prev_semester'] > 2) * 1.5 +
        (data['attendance_rate'] < 0.7) * 1 +
        (data['carryover_courses_count'] > 3) * 1.2 +
        (data['assignment_submission_rate'] < 0.8) * 0.8
    )
    
    # Convert to binary classification (0 = not at risk, 1 = at risk)
    academic_performance = (risk_score > 2).astype(int)
    data['academic_performance'] = academic_performance
    
    return pd.DataFrame(data)


def create_feature_importance_plot(
    pipeline: Any,
    X: pd.DataFrame,
    output_path: Path,
    top_n: int = 15
) -> None:
    """Create and save feature importance plot for top N features."""
    print(f"Creating feature importance plot for top {top_n} features...")
    
    # Get the model from pipeline
    model = pipeline.named_steps.get("model")
    
    # Extract feature names after preprocessing
    preprocessor = pipeline.named_steps.get("preprocessor")
    try:
        feature_names = preprocessor.get_feature_names_out().tolist()
    except Exception:
        feature_names = [f"feature_{i}" for i in range(X.shape[1])]
    
    # Get feature importance based on model type
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
    elif hasattr(model, 'coef_'):
        importances = np.abs(model.coef_).flatten()
    else:
        print("Model doesn't have feature_importances_ or coef_, skipping...")
        return
    
    # Create feature importance DataFrame
    feature_importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importances
    }).sort_values('importance', ascending=False)
    
    # Take top N features
    top_features = feature_importance_df.head(top_n)
    
    # Create plot
    plt.figure(figsize=(10, 8))
    bars = plt.barh(range(len(top_features)), top_features['importance'], 
                    color='#2E86AB', edgecolor='black', alpha=0.8)
    
    # Customize plot
    plt.yticks(range(len(top_features)), top_features['feature'])
    plt.xlabel('Feature Importance', fontweight='bold')
    plt.title(f'Top {top_n} Feature Importance - Random Forest Model', 
             fontweight='bold', pad=20)
    plt.grid(axis='x', alpha=0.3)
    
    # Add value labels on bars
    for i, (bar, importance) in enumerate(zip(bars, top_features['importance'])):
        plt.text(bar.get_width() + 0.001, bar.get_y() + bar.get_height()/2, 
                f'{importance:.3f}', ha='left', va='center', fontsize=8)
    
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Feature importance plot saved to: {output_path}")
    
    # Save feature importance data
    importance_data_path = output_path.parent / "feature_importance_data.json"
    with open(importance_data_path, 'w') as f:
        json.dump(top_features.to_dict('records'), f, indent=2)


def generate_shap_explanations(
    pipeline: Any,
    X: pd.DataFrame,
    y: pd.Series,
    output_dir: Path
) -> Dict[str, Any]:
    """Generate comprehensive SHAP explanations and save visualizations."""
    print("Generating SHAP explanations...")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Split data to get test set
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 1. Generate SHAP summary plot (global feature importance)
    summary_path = output_dir / "shap_global_summary.png"
    shap_summary_plot_for_pipeline(
        pipeline=pipeline,
        X=X_test,
        out_path=summary_path,
        max_display=20,
        title="SHAP Summary - Global Feature Importance"
    )
    print(f"SHAP summary plot saved to: {summary_path}")
    
    # 2. Generate SHAP waterfall plot for at-risk student
    # Find an at-risk student (prediction = 1)
    risk_indices = y_test[y_test == 1].index.tolist()
    if not risk_indices:
        print("No at-risk students found in test set, using first sample...")
        instance_index = 0
    else:
        # Convert to positional index within the test set
        original_index = risk_indices[0]
        instance_index = y_test.index.get_loc(original_index)
    
    waterfall_path = output_dir / "shap_local_waterfall.png"
    waterfall_result = shap_local_waterfall_for_pipeline(
        pipeline=pipeline,
        X=X_test,
        instance_index=instance_index,
        out_path=waterfall_path,
        max_display=15,
        title="SHAP Waterfall - At-Risk Student Explanation"
    )
    print(f"SHAP waterfall plot saved to: {waterfall_path}")
    
    # 3. Generate feature importance plot
    importance_path = output_dir / "feature_importance.png"
    create_feature_importance_plot(pipeline, X_test, importance_path, top_n=15)
    print(f"Feature importance plot saved to: {importance_path}")
    
    # 4. Generate summary statistics
    summary_stats = generate_summary_statistics(pipeline, X_test, y_test, waterfall_result)
    
    # Save summary statistics
    stats_path = output_dir / "explanation_summary.json"
    with open(stats_path, 'w') as f:
        json.dump(summary_stats, f, indent=2)
    print(f"Summary statistics saved to: {stats_path}")
    
    return summary_stats


def generate_summary_statistics(
    pipeline: Any,
    X: pd.DataFrame,
    y: pd.Series,
    waterfall_result: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate summary statistics for the explanations."""
    
    # Get model predictions
    y_pred = pipeline.predict(X)
    
    # Calculate basic metrics
    accuracy = (y_pred == y).mean()
    risk_students = (y == 1).sum()
    total_students = len(y)
    
    # Get feature names
    preprocessor = pipeline.named_steps.get("preprocessor")
    try:
        feature_names = preprocessor.get_feature_names_out().tolist()
    except Exception:
        feature_names = [f"feature_{i}" for i in range(X.shape[1])]
    
    summary = {
        "model_type": type(pipeline.named_steps.get("model")).__name__,
        "total_samples": total_students,
        "at_risk_students": int(risk_students),
        "risk_percentage": float(risk_students / total_students * 100),
        "accuracy": float(accuracy),
        "total_features": len(feature_names),
        "waterfall_explanation": {
            "instance_index": waterfall_result.get("instance_index"),
            "predicted_label": waterfall_result.get("predicted_label"),
            "top_positive_factors": waterfall_result.get("top_positive", {}),
            "top_negative_factors": waterfall_result.get("top_negative", {})
        }
    }
    
    return summary


def main() -> None:
    """Main function to generate SHAP explanations."""
    parser = argparse.ArgumentParser(
        description="Generate comprehensive SHAP explanations for academic reporting"
    )
    parser.add_argument(
        "--model",
        default="artifacts/random_forest/random_forest_pipeline.joblib",
        help="Path to trained model pipeline"
    )
    parser.add_argument(
        "--data",
        help="Path to dataset (optional, will generate synthetic data if not provided)"
    )
    parser.add_argument(
        "--target",
        default="academic_performance",
        help="Target column name"
    )
    parser.add_argument(
        "--output",
        default="artifacts/shap",
        help="Output directory for explanation files"
    )
    
    args = parser.parse_args()
    
    # Setup matplotlib for academic reporting
    setup_matplotlib_style()
    
    # Convert paths
    model_path = Path(args.model)
    data_path = Path(args.data) if args.data else None
    output_dir = Path(args.output)
    
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    
    print("=" * 60)
    print("Generating SHAP Explanations for Academic Reporting")
    print("=" * 60)
    
    # Load pipeline and data
    pipeline, X, y = load_pipeline_and_data(model_path, data_path, args.target)
    
    print(f"Dataset shape: {X.shape}")
    print(f"Target distribution: {y.value_counts().to_dict()}")
    print(f"Model type: {type(pipeline.named_steps.get('model')).__name__}")
    
    # Generate explanations
    summary_stats = generate_shap_explanations(pipeline, X, y, output_dir)
    
    print("=" * 60)
    print("SHAP Explanations Generated Successfully!")
    print("=" * 60)
    print(f"Output directory: {output_dir}")
    print(f"Files generated:")
    print(f"  - shap_global_summary.png")
    print(f"  - shap_local_waterfall.png") 
    print(f"  - feature_importance.png")
    print(f"  - explanation_summary.json")
    print(f"  - feature_importance_data.json")
    
    print(f"\nSummary Statistics:")
    print(f"  - Total samples: {summary_stats['total_samples']}")
    print(f"  - At-risk students: {summary_stats['at_risk_students']} ({summary_stats['risk_percentage']:.1f}%)")
    print(f"  - Model accuracy: {summary_stats['accuracy']:.3f}")
    print(f"  - Total features: {summary_stats['total_features']}")


if __name__ == "__main__":
    main()
