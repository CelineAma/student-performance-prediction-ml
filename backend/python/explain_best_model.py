from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import pandas as pd

from src.explainability import shap_local_waterfall_for_pipeline, shap_summary_plot_for_pipeline
from src.feature_engineering import BasicFeatureEngineer


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate global and local SHAP explanations for the best-performing model."
    )
    parser.add_argument(
        "--model",
        default="artifacts/random_forest/random_forest_pipeline.joblib",
        help="Path to the saved best model pipeline (.joblib)",
    )
    parser.add_argument(
        "--data",
        default="data/raw/synthetic_student_dataset.csv",
        help="Path to input CSV dataset",
    )
    parser.add_argument("--target", default="performance_risk", help="Target column name")
    parser.add_argument(
        "--out-dir",
        default="artifacts/shap",
        help="Directory to save SHAP plots and explanation summary",
    )
    parser.add_argument(
        "--max-display",
        type=int,
        default=20,
        help="Maximum number of features displayed in SHAP plots",
    )
    return parser.parse_args()


def _format_top_contributors(contrib: dict[str, float], direction: str, limit: int = 5) -> str:
    if not contrib:
        return f"No strong {direction} contributions were identified among the top features."

    items = sorted(contrib.items(), key=lambda kv: abs(kv[1]), reverse=True)[:limit]
    lines = [f"- {name}: {value:+.3f}" for name, value in items]
    return "\n".join(lines)


def main() -> None:
    args = parse_args()

    model_path = Path(args.model)
    data_path = Path(args.data)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    pipeline = joblib.load(model_path)

    df = pd.read_csv(data_path)
    if args.target not in df.columns:
        raise ValueError(f"Target column '{args.target}' not found in dataset columns.")

    # Apply the same minimal feature engineering used during training.
    fe = BasicFeatureEngineer(add_missing_count=True)
    df_fe = fe.transform(df)

    X = df_fe.drop(columns=[args.target])

    # ----------------------
    # Global explanation
    # ----------------------
    global_out = out_dir / "shap_global_summary.png"
    shap_summary_plot_for_pipeline(
        pipeline=pipeline,
        X=X,
        out_path=global_out,
        max_display=args.max_display,
        title="Global SHAP Summary (Overall Feature Influence)",
    )

    # ----------------------
    # Local explanation
    # ----------------------
    # Select an example student predicted as at-risk (label=1).
    preds = pipeline.predict(X)
    at_risk_indices = [int(i) for i in range(len(preds)) if int(preds[i]) == 1]

    if len(at_risk_indices) == 0:
        instance_index = 0
    else:
        instance_index = at_risk_indices[0]

    local_out = out_dir / "shap_local_waterfall_at_risk.png"
    local_info = shap_local_waterfall_for_pipeline(
        pipeline=pipeline,
        X=X,
        instance_index=instance_index,
        out_path=local_out,
        max_display=min(args.max_display, 15),
        title=f"Local SHAP Explanation (Student Index {instance_index})",
    )

    (out_dir / "local_explanation_summary.json").write_text(
        json.dumps(local_info, indent=2), encoding="utf-8"
    )

    # ----------------------
    # Educator-friendly academic interpretation
    # ----------------------
    # The SHAP value signs are interpreted as follows:
    # - Positive contributions increase the model's estimated risk of being at-risk.
    # - Negative contributions reduce the model's estimated risk.
    narrative = "\n".join(
        [
            "SHAP Explanation Summary (Educator-Facing Interpretation)",
            "",
            "1. Global feature importance (overall):",
            "- The global SHAP summary plot shows which variables most consistently influence predictions across the student population.",
            "- Features appearing at the top of the plot have the strongest overall association with the model’s risk estimates.",
            "- This should be interpreted as a descriptive model behaviour, not as proof of causal influence.",
            "",
            "2. Local explanation (single at-risk prediction):",
            f"- An example student record (index {local_info.get('instance_index')}) predicted as at-risk is explained using a SHAP waterfall plot.",
            "- The waterfall plot decomposes the prediction into contributions from each feature.",
            "- Positive contributions indicate factors that push the prediction toward ‘at risk’; negative contributions push it toward ‘not at risk’.",
            "",
            "Top factors increasing the at-risk prediction (examples):",
            _format_top_contributors(local_info.get("top_positive", {}), direction="positive"),
            "",
            "Top factors reducing the at-risk prediction (examples):",
            _format_top_contributors(local_info.get("top_negative", {}), direction="negative"),
            "",
            "Practical interpretation for non-technical educators:",
            "- The explanation highlights which measurable indicators (academic history and engagement proxies) are most aligned with increased predicted risk.",
            "- These indicators can support targeted academic advising (e.g., monitoring students with low prior performance and low engagement).",
            "- The output is intended for decision support and should be used alongside professional judgment and institutional policies.",
            "",
            f"Saved global plot: {global_out}",
            f"Saved local plot: {local_out}",
        ]
    )

    (out_dir / "educator_friendly_interpretation.txt").write_text(narrative, encoding="utf-8")

    print("Saved SHAP global summary to:", global_out)
    print("Saved SHAP local waterfall to:", local_out)
    print("Saved educator interpretation to:", out_dir / "educator_friendly_interpretation.txt")


if __name__ == "__main__":
    main()
