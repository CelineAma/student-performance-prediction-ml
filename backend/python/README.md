# Student Academic Performance Prediction (Python ML)

This folder contains a clean, CRISP-DM-aligned machine learning boilerplate for predicting student academic performance in Nigerian tertiary institutions.

## Recommended folder structure

- `data/raw/` : input CSV dataset(s)
- `artifacts/` : trained models, metrics, plots
- `src/` : reusable functions (preprocessing, modeling, evaluation, explainability)
- `train.py` : end-to-end training and evaluation
- `explain.py` : SHAP explainability for a saved model

## Quick start

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Place your dataset CSV in `data/raw/`.

4. Train models (Random Forest and LightGBM) and save outputs to `artifacts/`:

```bash
python train.py --data data/raw/dataset.csv --target target
```

5. Generate SHAP explanations for a saved model:

```bash
python explain.py --model artifacts/best_model.joblib --data data/raw/dataset.csv --target target
```

## Notes

- The scripts implement:
  - data preprocessing (imputation, scaling, one-hot encoding)
  - SMOTE for class imbalance (applied on the training split only)
  - model training (Random Forest, LightGBM)
  - evaluation (accuracy, F1, confusion matrix, ROC-AUC where applicable)
  - SHAP explainability (summary plot saved to `artifacts/`)

- Update `--target` to your dataset's target column name.
