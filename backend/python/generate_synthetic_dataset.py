from __future__ import annotations

import argparse
import math
import os
import uuid
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd


NIGERIAN_STATES = [
    "Abia",
    "Adamawa",
    "Akwa Ibom",
    "Anambra",
    "Bauchi",
    "Bayelsa",
    "Benue",
    "Borno",
    "Cross River",
    "Delta",
    "Ebonyi",
    "Edo",
    "Ekiti",
    "Enugu",
    "FCT",
    "Gombe",
    "Imo",
    "Jigawa",
    "Kaduna",
    "Kano",
    "Katsina",
    "Kebbi",
    "Kogi",
    "Kwara",
    "Lagos",
    "Nasarawa",
    "Niger",
    "Ogun",
    "Ondo",
    "Osun",
    "Oyo",
    "Plateau",
    "Rivers",
    "Sokoto",
    "Taraba",
    "Yobe",
    "Zamfara",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a synthetic Nigerian tertiary institution student dataset (CSV)."
    )
    parser.add_argument("--n", type=int, default=1200, help="Number of records (>= 1000 recommended)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    parser.add_argument(
        "--target-rate",
        type=float,
        default=0.15,
        help="Desired proportion of at-risk class (performance_risk=1)",
    )
    parser.add_argument(
        "--out",
        default=str(Path("data") / "raw" / "synthetic_student_dataset.csv"),
        help="Output CSV path",
    )
    return parser.parse_args()


def _sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def _choice(rng: np.random.Generator, values: List[str], p: List[float], size: int) -> np.ndarray:
    values_arr = np.array(values, dtype=object)
    p_arr = np.array(p, dtype=float)

    if len(values_arr) != len(p_arr):
        raise ValueError(
            f"Probability vector length ({len(p_arr)}) must match values length ({len(values_arr)})."
        )

    total = float(p_arr.sum())
    if not np.isfinite(total) or total <= 0.0:
        raise ValueError("Probabilities must sum to a positive finite value.")

    # Normalize to avoid numpy's strict sum-to-1 requirement and floating point issues.
    p_arr = p_arr / total

    return rng.choice(values_arr, p=p_arr, size=size)


def _clip(a: np.ndarray, lo: float, hi: float) -> np.ndarray:
    return np.minimum(np.maximum(a, lo), hi)


def _calibrate_intercept(logits_no_intercept: np.ndarray, target_rate: float) -> float:
    """Find intercept so that mean(sigmoid(logits + intercept)) ~= target_rate."""

    lo, hi = -20.0, 20.0
    for _ in range(60):
        mid = (lo + hi) / 2.0
        rate = float(_sigmoid(logits_no_intercept + mid).mean())
        if rate < target_rate:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def generate(n: int, seed: int, target_rate: float) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    institution_type = _choice(rng, ["Federal", "State", "Private"], [0.45, 0.40, 0.15], n)

    faculty = _choice(
        rng,
        ["Sciences", "Engineering", "Social Sciences", "Arts", "Management Sciences"],
        [0.28, 0.18, 0.22, 0.14, 0.18],
        n,
    )

    dept_by_faculty: Dict[str, List[str]] = {
        "Sciences": ["Computer Science", "Biochemistry", "Microbiology", "Physics", "Mathematics"],
        "Engineering": [
            "Civil Engineering",
            "Electrical Engineering",
            "Mechanical Engineering",
            "Chemical Engineering",
        ],
        "Social Sciences": ["Economics", "Political Science", "Sociology", "Psychology"],
        "Arts": ["English", "History", "Philosophy", "Linguistics"],
        "Management Sciences": ["Accounting", "Business Administration", "Banking and Finance"],
    }

    department = np.array([rng.choice(dept_by_faculty[f]) for f in faculty], dtype=object)

    level = rng.choice(np.array([100, 200, 300, 400, 500]), p=[0.22, 0.24, 0.22, 0.26, 0.06], size=n)

    entry_mode = _choice(rng, ["UTME", "DirectEntry", "Transfer"], [0.78, 0.18, 0.04], n)

    # Demographics
    sex = _choice(rng, ["Male", "Female"], [0.52, 0.48], n)

    # Age depends on level and entry mode (Direct Entry slightly older)
    base_age = 17 + (level // 100) + rng.normal(0, 1.3, size=n)
    base_age += np.where(entry_mode == "DirectEntry", rng.normal(2.0, 0.6, size=n), 0.0)
    base_age += np.where(entry_mode == "Transfer", rng.normal(1.5, 0.6, size=n), 0.0)
    age = _clip(np.round(base_age), 16, 35).astype(int)

    state_of_origin = _choice(
        rng,
        NIGERIAN_STATES,
        # Slightly higher sampling for high-population states (still realistic, not deterministic)
        [
            0.020,
            0.020,
            0.020,
            0.025,
            0.020,
            0.015,
            0.020,
            0.020,
            0.020,
            0.025,
            0.018,
            0.020,
            0.018,
            0.022,
            0.018,
            0.018,
            0.020,
            0.018,
            0.022,
            0.030,
            0.020,
            0.018,
            0.018,
            0.018,
            0.060,  # Lagos
            0.018,
            0.018,
            0.028,
            0.020,
            0.020,
            0.030,
            0.018,
            0.028,
            0.016,
            0.016,
            0.016,
            0.016,
        ],
        n,
    )

    residency_status = _choice(rng, ["OnCampus", "OffCampus"], [0.35, 0.65], n)
    socioeconomic_band = _choice(rng, ["Low", "Middle", "High"], [0.35, 0.50, 0.15], n)

    # Academic
    utme_score = _clip(rng.normal(220, 35, size=n), 120, 350)
    utme_score = np.round(utme_score).astype(int)

    post_utme_score = _clip(rng.normal(62, 10, size=n), 20, 95)
    post_utme_score = np.round(post_utme_score, 1)

    entry_qualification = np.where(entry_mode == "UTME", "SSCE", rng.choice(["ND", "HND", "Alevel"], p=[0.7, 0.1, 0.2], size=n))
    entry_qualification = np.where(entry_mode == "Transfer", rng.choice(["ND", "HND"], p=[0.8, 0.2], size=n), entry_qualification)

    # CGPA is correlated with UTME and socioeconomic band (small effect) + noise
    ses_effect = np.select(
        [socioeconomic_band == "Low", socioeconomic_band == "Middle", socioeconomic_band == "High"],
        [-0.10, 0.00, 0.10],
        default=0.0,
    )
    utme_scaled = (utme_score - 200) / 80.0

    # Simulate a 5.0 scale (common in Nigeria)
    cgpa = 2.9 + 0.45 * utme_scaled + ses_effect + rng.normal(0, 0.55, size=n)
    cumulative_cgpa = _clip(cgpa, 0.5, 4.9)
    cumulative_cgpa = np.round(cumulative_cgpa, 2)

    prev_semester_gpa = _clip(cumulative_cgpa + rng.normal(0, 0.35, size=n), 0.0, 5.0)
    prev_semester_gpa = np.round(prev_semester_gpa, 2)

    # Course load varies with level (slightly higher at lower/middle levels)
    base_units = np.select(
        [level == 100, level == 200, level == 300, level == 400, level == 500],
        [23, 24, 22, 20, 18],
        default=22,
    )
    course_load_units = _clip(base_units + rng.integers(-4, 5, size=n), 12, 28).astype(int)

    # Failures and carryovers inversely related to CGPA
    risk_signal = 3.2 - cumulative_cgpa
    carryover_courses_count = _clip(rng.poisson(lam=_clip(0.8 + 1.2 * risk_signal, 0.1, 5.0)), 0, 10).astype(int)
    failed_courses_prev_semester = _clip(rng.poisson(lam=_clip(0.5 + 1.0 * risk_signal, 0.05, 4.5)), 0, 8).astype(int)
    core_courses_failed_total = _clip(
        carryover_courses_count + rng.poisson(lam=_clip(0.6 + 0.8 * risk_signal, 0.05, 5.0)),
        0,
        12,
    ).astype(int)

    continuous_assessment_avg = _clip(22 + 6.0 * cumulative_cgpa + rng.normal(0, 5.5, size=n), 0, 40)
    continuous_assessment_avg = np.round(continuous_assessment_avg, 1)

    # Behavioural
    attendance_rate = _clip(0.55 + 0.10 * (cumulative_cgpa - 2.5) + rng.normal(0, 0.12, size=n), 0.05, 1.0)
    attendance_rate = np.round(attendance_rate, 2)

    library_visits_per_month = _clip(
        rng.poisson(lam=_clip(2.2 + 1.2 * (cumulative_cgpa - 2.0), 0.2, 10.0)), 0, 25
    ).astype(int)

    lms_logins_per_week = _clip(
        rng.poisson(lam=_clip(3.5 + 1.6 * (cumulative_cgpa - 2.0), 0.2, 14.0)), 0, 40
    ).astype(int)

    assignment_submission_rate = _clip(0.62 + 0.09 * (cumulative_cgpa - 2.5) + rng.normal(0, 0.14, size=n), 0.0, 1.0)
    assignment_submission_rate = np.round(assignment_submission_rate, 2)

    late_registration_flag = rng.binomial(1, p=_clip(0.18 + 0.08 * (socioeconomic_band == "Low"), 0.05, 0.35), size=n)

    financial_clearance_delay_days = _clip(
        rng.poisson(lam=_clip(1.0 + 2.2 * (socioeconomic_band == "Low") + 0.8 * late_registration_flag, 0.0, 12.0)),
        0,
        60,
    ).astype(int)

    disciplinary_case_flag = rng.binomial(1, p=_clip(0.03 + 0.02 * (attendance_rate < 0.35), 0.01, 0.10), size=n)

    counselling_visits_semester = _clip(
        rng.poisson(lam=_clip(0.25 + 0.35 * (risk_signal > 0.8) + 0.15 * disciplinary_case_flag, 0.0, 3.0)),
        0,
        12,
    ).astype(int)

    medical_leave_flag = rng.binomial(1, p=0.03, size=n)

    # Construct at-risk label from a transparent logit combining academic + behavioural signals
    # (This produces statistical realism: risk increases with low CGPA, low attendance, carryovers, etc.)
    logits = (
        -1.2 * (cumulative_cgpa - 2.5)
        - 1.0 * (attendance_rate - 0.7)
        + 0.35 * carryover_courses_count
        + 0.25 * failed_courses_prev_semester
        + 0.03 * financial_clearance_delay_days
        - 0.8 * (assignment_submission_rate - 0.7)
        + 0.15 * late_registration_flag
        + 0.10 * disciplinary_case_flag
        + rng.normal(0, 0.35, size=n)
    )

    intercept = _calibrate_intercept(logits, target_rate=target_rate)
    prob_risk = _sigmoid(logits + intercept)
    performance_risk = rng.binomial(1, p=_clip(prob_risk, 0.001, 0.999), size=n).astype(int)

    student_id_hash = np.array([uuid.uuid4().hex for _ in range(n)], dtype=object)

    df = pd.DataFrame(
        {
            "student_id_hash": student_id_hash,
            "institution_type": institution_type,
            "faculty": faculty,
            "department": department,
            "level": level,
            "entry_mode": entry_mode,
            "age": age,
            "sex": sex,
            "state_of_origin": state_of_origin,
            "residency_status": residency_status,
            "socioeconomic_band": socioeconomic_band,
            "utme_score": utme_score,
            "post_utme_score": post_utme_score,
            "entry_qualification": entry_qualification,
            "prev_semester_gpa": prev_semester_gpa,
            "cumulative_cgpa": cumulative_cgpa,
            "carryover_courses_count": carryover_courses_count,
            "failed_courses_prev_semester": failed_courses_prev_semester,
            "core_courses_failed_total": core_courses_failed_total,
            "course_load_units": course_load_units,
            "continuous_assessment_avg": continuous_assessment_avg,
            "attendance_rate": attendance_rate,
            "library_visits_per_month": library_visits_per_month,
            "lms_logins_per_week": lms_logins_per_week,
            "assignment_submission_rate": assignment_submission_rate,
            "late_registration_flag": late_registration_flag,
            "financial_clearance_delay_days": financial_clearance_delay_days,
            "disciplinary_case_flag": disciplinary_case_flag,
            "counselling_visits_semester": counselling_visits_semester,
            "medical_leave_flag": medical_leave_flag,
            "performance_risk": performance_risk,
        }
    )

    return df


def main() -> None:
    args = parse_args()

    if args.n < 1000:
        raise ValueError("n must be at least 1000 to satisfy the project constraint.")
    if not (0.01 <= args.target_rate <= 0.50):
        raise ValueError("target-rate must be between 0.01 and 0.50")

    df = generate(n=args.n, seed=args.seed, target_rate=args.target_rate)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(out_path, index=False)

    # Print a brief summary to support quick validation
    counts = df["performance_risk"].value_counts(dropna=False).to_dict()
    total = len(df)
    rate = float(counts.get(1, 0)) / float(total) if total else 0.0

    print(f"Saved: {out_path}")
    print(f"Rows: {total}")
    print(f"Class counts: {counts}")
    print(f"At-risk rate: {rate:.3f}")


if __name__ == "__main__":
    main()
