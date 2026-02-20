from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import pandas as pd

from src.explainability import shap_summary_plot_for_pipeline
from src.feature_engineering import BasicFeatureEngineer


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate SHAP explanations for a saved model pipeline.")
    parser.add_argument("--model", required=True, help="Path to a saved .joblib pipeline")
    parser.add_argument("--data", required=True, help="Path to input CSV dataset")
    parser.add_argument("--target", required=True, help="Target column name")
    parser.add_argument("--out", default="artifacts/shap_summary.png", help="Output path for SHAP plot")
    parser.add_argument("--max-display", type=int, default=20)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    model_path = Path(args.model)
    out_path = Path(args.out)

    pipeline = joblib.load(model_path)

    df = pd.read_csv(Path(args.data))
    if args.target not in df.columns:
        raise ValueError(f"Target column '{args.target}' not found in dataset columns.")

    # Apply the same minimal feature engineering used during training
    fe = BasicFeatureEngineer(add_missing_count=True)
    df_fe = fe.transform(df)

    X = df_fe.drop(columns=[args.target])

    shap_summary_plot_for_pipeline(
        pipeline=pipeline,
        X=X,
        out_path=out_path,
        max_display=args.max_display,
        title="SHAP Summary (Tree Model)",
    )


if __name__ == "__main__":
    main()
