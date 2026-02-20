from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import GridSearchCV

from src.feature_engineering import BasicFeatureEngineer
from src.preprocessing import build_preprocessor_from_dataframe, split_train_test


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train a Random Forest classifier with SMOTE and report evaluation metrics."
    )
    parser.add_argument("--data", required=True, help="Path to input CSV dataset")
    parser.add_argument("--target", required=True, help="Target column name")
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--random-state", type=int, default=42)
    parser.add_argument(
        "--artifacts-dir",
        default="artifacts/random_forest",
        help="Directory to save model and evaluation artifacts",
    )
    return parser.parse_args()


def _metric_bundle(y_true: pd.Series, y_pred: np.ndarray) -> dict:
    # For imbalanced binary classification, reporting the positive class metrics is defensible.
    # If the dataset is multi-class, macro averaging is applied.
    unique = pd.Series(y_true).dropna().unique()
    is_binary = len(unique) == 2

    if is_binary:
        precision = float(precision_score(y_true, y_pred, pos_label=1, zero_division=0))
        recall = float(recall_score(y_true, y_pred, pos_label=1, zero_division=0))
        f1 = float(f1_score(y_true, y_pred, pos_label=1, zero_division=0))
        f1_macro = float(f1_score(y_true, y_pred, average="macro", zero_division=0))
    else:
        precision = float(precision_score(y_true, y_pred, average="macro", zero_division=0))
        recall = float(recall_score(y_true, y_pred, average="macro", zero_division=0))
        f1 = float(f1_score(y_true, y_pred, average="macro", zero_division=0))
        f1_macro = f1

    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "f1_macro": f1_macro,
    }


def main() -> None:
    args = parse_args()

    data_path = Path(args.data)
    artifacts_dir = Path(args.artifacts_dir)
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(data_path)

    # Feature engineering (minimal, consistent with the project pipeline)
    fe = BasicFeatureEngineer(add_missing_count=True)
    df = fe.transform(df)

    # Split first (prevents leakage)
    X_train, X_test, y_train, y_test = split_train_test(
        df=df,
        target=args.target,
        test_size=args.test_size,
        random_state=args.random_state,
        stratify=True,
    )

    preprocessor = build_preprocessor_from_dataframe(
        df=pd.concat([X_train, y_train], axis=1),
        target=args.target,
    )

    rf = RandomForestClassifier(
        random_state=args.random_state,
        n_jobs=-1,
    )

    # Pipeline order is important:
    # - preprocessing (impute/encode/scale)
    # - SMOTE (resampling on training data only, executed within fit)
    # - model
    pipe = ImbPipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("smote", SMOTE(random_state=args.random_state)),
            ("model", rf),
        ]
    )

    # Hyperparameter selection
    # A small grid is used to keep the approach computationally feasible and defensible.
    param_grid = {
        "model__n_estimators": [300, 500],
        "model__max_depth": [None, 8, 16],
        "model__min_samples_split": [2, 5],
        "model__min_samples_leaf": [1, 2],
        "model__max_features": ["sqrt", 0.5],
    }

    search = GridSearchCV(
        estimator=pipe,
        param_grid=param_grid,
        scoring="f1_macro",
        cv=5,
        n_jobs=-1,
        verbose=0,
    )

    search.fit(X_train, y_train)

    best_model = search.best_estimator_
    y_pred = best_model.predict(X_test)

    metrics = _metric_bundle(y_test, y_pred)

    # Save metrics
    metrics_payload = {
        "best_params": search.best_params_,
        "cv_best_score_f1_macro": float(search.best_score_),
        "test_metrics": metrics,
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
        "random_state": int(args.random_state),
        "test_size": float(args.test_size),
    }

    (artifacts_dir / "metrics.json").write_text(
        json.dumps(metrics_payload, indent=2), encoding="utf-8"
    )

    # Save the full pipeline
    joblib.dump(best_model, artifacts_dir / "random_forest_pipeline.joblib")

    # Feature importance extraction
    # The importance values correspond to the post-preprocessing feature space.
    pre = best_model.named_steps["preprocessor"]
    model = best_model.named_steps["model"]

    feature_names: list[str]
    try:
        feature_names = pre.get_feature_names_out().tolist()
    except Exception:
        feature_names = [f"feature_{i}" for i in range(int(model.feature_importances_.shape[0]))]

    importances = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": model.feature_importances_.astype(float),
        }
    ).sort_values("importance", ascending=False)

    importances.to_csv(artifacts_dir / "feature_importance.csv", index=False)

    # Print a concise console summary for quick reporting
    print("\nBest hyperparameters:")
    print(search.best_params_)
    print("\nTest set metrics:")
    for k, v in metrics.items():
        print(f"- {k}: {v:.4f}")


if __name__ == "__main__":
    main()
