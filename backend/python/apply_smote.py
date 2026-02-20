from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from imblearn.over_sampling import SMOTE

from src.preprocessing import build_preprocessor_from_dataframe, split_train_test


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Apply SMOTE to the training split only and report class distributions (before vs after)."
    )
    parser.add_argument("--data", required=True, help="Path to input CSV dataset")
    parser.add_argument("--target", required=True, help="Target column name")
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--random-state", type=int, default=42)
    parser.add_argument(
        "--out-dir",
        default="artifacts/smote",
        help="Directory to save resampled training data (optional)",
    )
    return parser.parse_args()


def _class_table(y: pd.Series) -> pd.DataFrame:
    counts = y.value_counts(dropna=False).sort_index()
    perc = (counts / len(y) * 100).round(2)
    return pd.DataFrame({"count": counts, "percent": perc})


def main() -> None:
    args = parse_args()

    df = pd.read_csv(Path(args.data))

    # 1) Split first to avoid leakage.
    X_train, X_test, y_train, y_test = split_train_test(
        df=df,
        target=args.target,
        test_size=args.test_size,
        random_state=args.random_state,
        stratify=True,
    )

    print("\nClass distribution BEFORE SMOTE (training split):")
    print(_class_table(y_train).to_string())

    # 2) Fit preprocessing on training split only.
    preprocessor = build_preprocessor_from_dataframe(
        df=pd.concat([X_train, y_train], axis=1),
        target=args.target,
    )
    preprocessor.fit(X_train)

    X_train_t = preprocessor.transform(X_train)

    # 3) Apply SMOTE on training data only.
    smote = SMOTE(random_state=args.random_state)
    X_res, y_res = smote.fit_resample(X_train_t, y_train)

    y_res = pd.Series(y_res, name=args.target)

    print("\nClass distribution AFTER SMOTE (resampled training split):")
    print(_class_table(y_res).to_string())

    # Optional: save the resampled arrays as CSV for auditability.
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    feature_names = []
    try:
        feature_names = preprocessor.get_feature_names_out().tolist()
    except Exception:
        feature_names = []

    pd.DataFrame(X_res, columns=feature_names if feature_names else None).to_csv(
        out_dir / "X_train_smote.csv", index=False
    )
    y_res.to_frame().to_csv(out_dir / "y_train_smote.csv", index=False)

    print(f"\nSaved resampled training data to: {out_dir}")


if __name__ == "__main__":
    main()
