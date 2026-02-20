from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split

from src.evaluation import evaluate_classifier, save_confusion_matrix, save_metrics, save_roc_curve
from src.feature_engineering import BasicFeatureEngineer
from src.modeling import build_lightgbm_pipeline, build_random_forest_pipeline
from src.preprocessing import build_preprocessor, infer_feature_types


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train RF and LightGBM models with SMOTE and evaluate.")
    parser.add_argument("--data", required=True, help="Path to input CSV dataset")
    parser.add_argument("--target", required=True, help="Target column name")
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--random-state", type=int, default=42)
    parser.add_argument("--artifacts-dir", default="artifacts", help="Where to save models/metrics")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data_path = Path(args.data)
    artifacts_dir = Path(args.artifacts_dir)
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(data_path)
    if args.target not in df.columns:
        raise ValueError(f"Target column '{args.target}' not found in dataset columns.")

    # CRISP-DM: Data Preparation (basic feature engineering + preprocessing)
    fe = BasicFeatureEngineer(add_missing_count=True)
    df_fe = fe.transform(df)

    X = df_fe.drop(columns=[args.target])
    y = df_fe[args.target]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=args.test_size,
        random_state=args.random_state,
        stratify=y if y.nunique() > 1 else None,
    )

    spec = infer_feature_types(pd.concat([X_train, y_train], axis=1), target=args.target)
    preprocessor = build_preprocessor(spec)

    model_specs = [
        build_random_forest_pipeline(preprocessor, random_state=args.random_state),
        build_lightgbm_pipeline(preprocessor, random_state=args.random_state),
    ]

    best_name = None
    best_f1 = -1.0
    best_path = artifacts_dir / "best_model.joblib"

    for ms in model_specs:
        ms.pipeline.fit(X_train, y_train)

        y_pred = ms.pipeline.predict(X_test)
        y_proba = None
        if hasattr(ms.pipeline, "predict_proba"):
            try:
                y_proba = ms.pipeline.predict_proba(X_test)
            except Exception:
                y_proba = None

        result = evaluate_classifier(y_test, y_pred, y_proba=y_proba)

        # Save artifacts
        model_path = artifacts_dir / f"{ms.name}.joblib"
        joblib.dump(ms.pipeline, model_path)

        metrics_path = artifacts_dir / f"{ms.name}_metrics.json"
        save_metrics(result, metrics_path)

        cm_path = artifacts_dir / f"{ms.name}_confusion_matrix.png"
        save_confusion_matrix(y_test, y_pred, cm_path, title=f"Confusion Matrix: {ms.name}")

        if y_proba is not None:
            if (hasattr(y_proba, "ndim") and y_proba.ndim == 1) or (
                hasattr(y_proba, "shape") and len(y_proba.shape) == 2 and y_proba.shape[1] == 2
            ):
                proba_pos = y_proba if y_proba.ndim == 1 else y_proba[:, 1]
                roc_path = artifacts_dir / f"{ms.name}_roc_curve.png"
                save_roc_curve(y_test, proba_pos, roc_path, title=f"ROC Curve: {ms.name}")

        f1_macro = float(result.metrics.get("f1_macro", 0.0))
        if f1_macro > best_f1:
            best_f1 = f1_macro
            best_name = ms.name
            joblib.dump(ms.pipeline, best_path)

    (artifacts_dir / "best_model_name.txt").write_text(str(best_name), encoding="utf-8")


if __name__ == "__main__":
    main()
