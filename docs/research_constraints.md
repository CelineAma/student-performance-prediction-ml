# Research Constraints

## Dataset Limitations
- **Representativeness**: Datasets obtained from a single institution, department, or session may not fully represent the diversity of Nigerian tertiary institutions (e.g., federal, state, and private institutions), thereby limiting generalisability.
- **Data quality and missingness**: Student records may contain missing, inconsistent, or delayed entries due to manual processes and heterogeneous information systems.
- **Feature availability**: Potentially important predictors (e.g., detailed attendance logs, continuous assessment breakdowns, learning management system interactions) may be unavailable or incomplete.
- **Temporal drift**: Changes in curriculum, grading policies, admission standards, or instructional delivery can alter relationships between predictors and outcomes over time, reducing out-of-time performance.
- **Label definition**: Academic outcomes may be operationalised in different ways (e.g., GPA bands, degree classification categories, pass/fail), which affects class balance, metric choice, and interpretation.

## Ethical Considerations
- **Privacy and confidentiality**: Student data should be anonymised or pseudonymised, and direct identifiers (e.g., names, matriculation numbers) excluded from modeling.
- **Informed use**: The system should be presented as decision support rather than a deterministic judgment of student ability.
- **Fairness and bias**: Socio-economic or demographic features may embed structural inequities. Their inclusion requires careful justification, bias assessment, and transparency in reporting.
- **Data governance**: Access should follow institutional approvals and appropriate data handling practices, including secure storage and restricted access.

## Interpretability Requirement
- **Stakeholder acceptability**: Academic advisers and administrators typically require understandable reasons behind predictions to support intervention planning.
- **Accountability**: Interpretability supports auditability and helps identify spurious correlations or data leakage.
- **Methodological transparency**: The project prioritises model explanations at both global (feature importance patterns) and local (individual prediction contributions) levels using SHAP.

## Deployment Constraints
- **Operational simplicity**: The deployed system should be lightweight and feasible on typical institutional hardware or low-cost cloud hosting.
- **Maintainability**: The solution should allow model updates when new cohorts are available and support reproducible retraining.
- **Latency and reliability**: Predictions should be returned quickly for interactive use, with clear handling of invalid or missing inputs.
- **Security**: The API surface should be minimal, with input validation and secure handling of any uploaded data.
