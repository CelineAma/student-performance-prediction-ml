# Modeling Decisions

## Why Random Forest and LightGBM
- **Performance on tabular data**: Both algorithms are strong baselines for structured, tabular datasets commonly found in academic records.
- **Robustness**: Random Forest reduces variance through bagging and typically performs well with minimal tuning; this is suitable for undergraduate-level methodological reliability.
- **Efficiency and accuracy**: LightGBM is a gradient boosting framework designed for efficient training and competitive predictive performance, particularly when feature interactions are present.
- **Complementary comparison**: Using a bagging method (Random Forest) and a boosting method (LightGBM) supports a balanced comparative study and strengthens empirical justification.

## Why SMOTE
- **Addressing class imbalance**: Academic risk prediction often involves minority classes (e.g., students at risk of failure). Standard learners can underperform on minority outcomes.
- **Training-only application**: SMOTE is applied only to the training split to reduce bias without leaking information from the test set.
- **Practicality**: SMOTE is widely used and straightforward to implement, making it appropriate for a transparent undergraduate methodology.

## Why SHAP
- **Consistency and comparability**: SHAP provides feature-attribution explanations grounded in game theory, enabling consistent interpretation across different tree-based models.
- **Global and local explanations**: The method supports both aggregate understanding (summary plots) and case-level reasoning (individual contributions), aligning with educational decision-support needs.
- **Auditability**: SHAP helps identify unexpected drivers of predictions, supporting error analysis and responsible reporting.

## Why Node.js + Python Architecture
- **Separation of concerns**: Python is used for model training, evaluation, and explainability due to mature ML libraries; Node.js serves the web and API layer due to strong ecosystem support for web application development.
- **Maintainability**: A service boundary allows the ML component to be updated independently of the frontend and general backend logic.
- **Deployment flexibility**: The architecture supports multiple deployment patterns, including a Python model service (e.g., REST endpoint) behind a Node.js server, or offline training with model artefact loading for inference.
- **Educational alignment**: The stack reflects practical industry patterns while remaining implementable within undergraduate project constraints.
