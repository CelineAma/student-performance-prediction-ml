
# Dataset Schema and Feature Description

## Overview
This section presents the dataset schema used for predicting student academic performance in Nigerian tertiary institutions. The dataset is structured in a tabular format (CSV), where each row represents an individual undergraduate student record and each column represents a measured attribute (predictor) or the target outcome. The schema is designed to support:

- academic-risk prediction for early intervention;
- mixed data types (numerical and categorical), consistent with institutional records;
- interpretability, by retaining features that are educationally plausible and reportable.

## Target Variable Definition
- **Target column name**: `performance_risk`
- **Type**: Categorical (binary)
- **Definition**:
  - `0` = Not at risk (expected to pass/maintain satisfactory academic standing)
  - `1` = At risk (likely to fail key courses, be on probation, or experience significant academic decline)

This target definition supports proactive academic advising and aligns with the objective of identifying students at risk of poor performance.

## Class Distribution (Imbalanced Outcome)
In realistic tertiary institution settings, most students are not academically at risk. The dataset is therefore expected to be imbalanced.

- **Not at risk (`0`)**: approximately 80% to 90%
- **At risk (`1`)**: approximately 10% to 20%

For reporting and experimental design in this project, a representative distribution is:

- **Not at risk (`0`)**: 85%
- **At risk (`1`)**: 15%

This imbalance motivates the use of SMOTE on the training split during model development.

## Feature Schema (CSV Columns)
The features are grouped into academic, demographic, behavioural, and limited administrative/context variables. Direct identifiers (e.g., names, matriculation numbers, phone numbers) are excluded.

| Column name | Data type | Category | Description |
|---|---|---|---|
| `student_id_hash` | string | Administrative | Anonymised unique identifier (hashed). Used for record management; excluded from model training features. |
| `institution_type` | categorical | Context | Institution ownership type: `Federal`, `State`, `Private`. |
| `faculty` | categorical | Context | Faculty grouping (e.g., Sciences, Engineering, Social Sciences). |
| `department` | categorical | Context | Department or programme of study (e.g., Computer Science, Accounting). |
| `level` | integer | Context | Current level of study (100, 200, 300, 400, 500). |
| `entry_mode` | categorical | Context | Mode of admission: `UTME`, `DirectEntry`, `Transfer`. |
| `age` | integer | Demographic | Student age at the start of the session/semester. |
| `sex` | categorical | Demographic | Sex recorded by the institution: `Male`, `Female`. |
| `state_of_origin` | categorical | Demographic | Nigerian state of origin (36 states + FCT). |
| `residency_status` | categorical | Demographic | Place of residence: `OnCampus`, `OffCampus`. |
| `socioeconomic_band` | categorical | Demographic | Proxy socioeconomic grouping: `Low`, `Middle`, `High` (requires ethical justification and bias checks). |
| `utme_score` | integer | Academic | UTME score (typically 0–400), where available. |
| `post_utme_score` | float | Academic | Post-UTME screening score (institution-specific scale), where available. |
| `entry_qualification` | categorical | Academic | Highest entry qualification: `SSCE`, `ND`, `HND`, `Alevel`. |
| `prev_semester_gpa` | float | Academic | Previous semester GPA (scale depends on institution, e.g., 0.00–5.00). |
| `cumulative_cgpa` | float | Academic | Cumulative CGPA up to previous semester. |
| `carryover_courses_count` | integer | Academic | Number of registered carryover courses. |
| `failed_courses_prev_semester` | integer | Academic | Number of failed courses in the previous semester. |
| `core_courses_failed_total` | integer | Academic | Total number of failed compulsory/core courses to date. |
| `course_load_units` | integer | Academic | Total registered credit units for the current semester. |
| `continuous_assessment_avg` | float | Academic | Average continuous assessment score for current semester (e.g., 0–40), where available. |
| `attendance_rate` | float | Behavioural | Class attendance proportion (0–1), derived from attendance registers where available. |
| `library_visits_per_month` | integer | Behavioural | Average monthly library visits (engagement proxy). |
| `lms_logins_per_week` | integer | Behavioural | Weekly LMS/portal login frequency, where applicable. |
| `assignment_submission_rate` | float | Behavioural | Proportion of assignments submitted by deadlines (0–1), where available. |
| `late_registration_flag` | integer (0/1) | Behavioural | Indicates late registration of courses (planning/administrative delay proxy). |
| `financial_clearance_delay_days` | integer | Behavioural | Days delayed in completing fee/clearance processes (resource/administrative proxy). |
| `disciplinary_case_flag` | integer (0/1) | Behavioural | Indicates recorded disciplinary issues (sensitive; include only with approval and clear justification). |
| `counselling_visits_semester` | integer | Support/Health (Optional) | Number of counselling unit visits (sensitive; privacy considerations apply). |
| `medical_leave_flag` | integer (0/1) | Support/Health (Optional) | Whether the student took approved medical leave during the semester. |
| `performance_risk` | categorical (0/1) | Target | Outcome label indicating academic risk status (defined above). |

## Notes for Methodological Reporting
- The selected variables are intended to be realistic for Nigerian tertiary institutions, but availability may vary across institutions.
- Sensitive features (e.g., disciplinary and counselling indicators) should only be used when ethically approved and where inclusion can be justified without discriminatory impact.
- The presence of mixed data types justifies a preprocessing pipeline (imputation, encoding, and scaling) and supports the use of tree-based models (Random Forest and LightGBM).
