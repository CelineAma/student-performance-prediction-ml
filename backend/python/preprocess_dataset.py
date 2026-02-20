from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.preprocessing import build_preprocessor_from_dataframe, split_train_test


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preprocess the student dataset (impute, encode, scale) with a train-test split."
    )
    parser.add_argument("--data", required=True, help="Path to input CSV dataset")
    parser.add_argument("--target", required=True, help="Target column name")
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--random-state", type=int, default=42)
    parser.add_argument(
        "--out-dir",
        default="artifacts/preprocessing",
        help="Directory to save transformed arrays as CSV (optional) and feature names",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    data_path = Path(args.data)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(data_path)

    # 1) Train-test split (performed before fitting preprocessing steps)
    X_train, X_test, y_train, y_test = split_train_test(
        df=df,
        target=args.target,
        test_size=args.test_size,
        random_state=args.random_state,
        stratify=True,
    )

    # 2) Build preprocessing pipeline:
    #    - numeric: median imputation + standard scaling
    #    - categorical: most-frequent imputation + one-hot encoding
    preprocessor = build_preprocessor_from_dataframe(
        df=pd.concat([X_train, y_train], axis=1),
        target=args.target,
    )

    # 3) Fit on training data only (prevents test-set leakage)
    preprocessor.fit(X_train)

    # 4) Transform both splits using the fitted preprocessor
    X_train_t = preprocessor.transform(X_train)
    X_test_t = preprocessor.transform(X_test)

    # Persist feature names for reporting / debugging
    feature_names = []
    try:
        feature_names = preprocessor.get_feature_names_out().tolist()
    except Exception:
        feature_names = []

    (out_dir / "feature_names.txt").write_text("\n".join(feature_names), encoding="utf-8")

    # Save transformed arrays as CSV for inspection (optional but useful in an academic project)
    pd.DataFrame(X_train_t, columns=feature_names if feature_names else None).to_csv(
        out_dir / "X_train_transformed.csv", index=False
    )
    pd.DataFrame(X_test_t, columns=feature_names if feature_names else None).to_csv(
        out_dir / "X_test_transformed.csv", index=False
    )
    y_train.to_frame(name=args.target).to_csv(out_dir / "y_train.csv", index=False)
    y_test.to_frame(name=args.target).to_csv(out_dir / "y_test.csv", index=False)

    print("Saved preprocessing outputs to:", out_dir)
    print("X_train transformed shape:", getattr(X_train_t, "shape", None))
    print("X_test transformed shape:", getattr(X_test_t, "shape", None))


if __name__ == "__main__":
    main()
