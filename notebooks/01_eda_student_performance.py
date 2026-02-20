from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def _pct(series: pd.Series) -> pd.Series:
    return (series / series.sum() * 100).round(2)


def main() -> None:
    """Exploratory Data Analysis (EDA) for the student performance dataset.

    This script is written in a notebook-style structure for readability and for
    straightforward conversion to a Jupyter notebook if desired.
    """

    sns.set_theme(style="whitegrid")

    data_path = Path("data") / "raw" / "synthetic_student_dataset.csv"
    target_col = "performance_risk"

    df = pd.read_csv(data_path)

    print("\n" + "=" * 80)
    print("EXPLORATORY DATA ANALYSIS (EDA): STUDENT ACADEMIC PERFORMANCE DATASET")
    print("=" * 80)
    print(f"Dataset path: {data_path}")
    print(f"Shape (rows, columns): {df.shape}")

    # ---------------------------------------------------------------------
    # 1. Descriptive Statistics
    # ---------------------------------------------------------------------
    print("\n" + "-" * 80)
    print("1. DESCRIPTIVE STATISTICS")
    print("-" * 80)

    # Academic note:
    # Descriptive statistics provide evidence on scale consistency, central
    # tendencies, dispersion, and potential outliers. These summaries support
    # transparent reporting prior to model development.

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    numeric_desc = df[numeric_cols].describe().T
    numeric_desc["missing"] = df[numeric_cols].isna().sum().values
    numeric_desc["missing_rate"] = (numeric_desc["missing"] / len(df)).round(4)

    print("\nNumeric feature summary (describe + missingness):")
    print(numeric_desc.to_string())

    categorical_cols = df.select_dtypes(exclude=["number"]).columns.tolist()
    categorical_cols = [c for c in categorical_cols if c not in ["student_id_hash"]]

    print("\nSelected categorical distributions (top categories):")
    for c in [
        "institution_type",
        "faculty",
        "department",
        "level",
        "entry_mode",
        "sex",
        "state_of_origin",
        "residency_status",
        "socioeconomic_band",
    ]:
        if c in df.columns:
            counts = df[c].value_counts(dropna=False)
            table = pd.DataFrame({"count": counts, "percent": _pct(counts)})
            print(f"\n{c}:")
            print(table.head(15).to_string())

    # ---------------------------------------------------------------------
    # 2. Missing Value Analysis
    # ---------------------------------------------------------------------
    print("\n" + "-" * 80)
    print("2. MISSING VALUE ANALYSIS")
    print("-" * 80)

    missing_counts = df.isna().sum().sort_values(ascending=False)
    missing_rates = (missing_counts / len(df)).sort_values(ascending=False)
    missing_summary = pd.DataFrame({"missing": missing_counts, "missing_rate": missing_rates})

    print("\nMissingness summary (top 20 features):")
    print(missing_summary.head(20).to_string())

    plt.figure(figsize=(10, 6))
    plot_df = missing_summary[missing_summary["missing"] > 0].head(25)
    if len(plot_df) == 0:
        plt.text(0.5, 0.5, "No missing values detected in the dataset.", ha="center", va="center")
        plt.axis("off")
    else:
        sns.barplot(x=plot_df["missing"].values, y=plot_df.index)
        plt.title("Missing Values by Feature (Top 25)")
        plt.xlabel("Number of missing values")
        plt.ylabel("Feature")
    plt.tight_layout()
    plt.show()

    # ---------------------------------------------------------------------
    # 3. Target Distribution (Class Imbalance)
    # ---------------------------------------------------------------------
    print("\n" + "-" * 80)
    print("3. TARGET DISTRIBUTION (CLASS IMBALANCE)")
    print("-" * 80)

    if target_col not in df.columns:
        raise KeyError(f"Target column '{target_col}' was not found in the dataset.")

    target_counts = df[target_col].value_counts(dropna=False).sort_index()
    target_table = pd.DataFrame({"count": target_counts, "percent": _pct(target_counts)})

    print("\nTarget class distribution:")
    print(target_table.to_string())

    plt.figure(figsize=(6, 4))
    ax = sns.barplot(x=target_table.index.astype(str), y=target_table["count"].values)
    plt.title("Target Class Distribution")
    plt.xlabel(target_col)
    plt.ylabel("Count")
    for i, v in enumerate(target_table["count"].values):
        ax.text(i, v + max(target_table["count"].values) * 0.01, str(int(v)), ha="center")
    plt.tight_layout()
    plt.show()

    # Academic note:
    # Under class imbalance, accuracy alone can overstate performance. It is
    # therefore methodologically appropriate to report additional metrics such
    # as macro F1-score and to apply class balancing techniques (e.g., SMOTE)
    # on the training split only.

    # ---------------------------------------------------------------------
    # 4. Feature Correlations (Numerical Variables)
    # ---------------------------------------------------------------------
    print("\n" + "-" * 80)
    print("4. FEATURE CORRELATIONS (NUMERICAL VARIABLES)")
    print("-" * 80)

    numeric_df = df.select_dtypes(include=["number"]).copy()

    corr_cols = [c for c in numeric_df.columns if c != target_col]
    corr = numeric_df[corr_cols].corr(method="pearson")

    plt.figure(figsize=(12, 9))
    sns.heatmap(corr, cmap="coolwarm", center=0.0, linewidths=0.5)
    plt.title("Pearson Correlation Heatmap (Numeric Predictors)")
    plt.tight_layout()
    plt.show()

    # Report highly correlated pairs for academic discussion
    threshold = 0.70
    pairs = []
    for i in range(len(corr_cols)):
        for j in range(i + 1, len(corr_cols)):
            r = float(corr.iloc[i, j])
            if abs(r) >= threshold:
                pairs.append((corr_cols[i], corr_cols[j], r))

    high_corr = pd.DataFrame(pairs, columns=["feature_1", "feature_2", "pearson_r"])
    high_corr = high_corr.reindex(high_corr["pearson_r"].abs().sort_values(ascending=False).index)

    print(f"\nHighly correlated numeric feature pairs (|r| >= {threshold}):")
    if len(high_corr) == 0:
        print("No feature pairs exceeded the correlation threshold.")
    else:
        print(high_corr.head(30).to_string(index=False))

    # ---------------------------------------------------------------------
    # 5. Academic Interpretation of Key Observations
    # ---------------------------------------------------------------------
    print("\n" + "-" * 80)
    print("5. ACADEMIC INTERPRETATION OF KEY OBSERVATIONS")
    print("-" * 80)

    missing_total = int(df.isna().sum().sum())
    at_risk_rate = float(target_table.loc[1, "percent"]) if 1 in target_table.index else 0.0

    print(
        "\nDataset completeness:\n"
        f"- The dataset contains N = {len(df)} records and p = {df.shape[1]} variables. "
        f"The total number of missing entries is {missing_total}. "
        "This evidence supports the imputation strategy described in the methodology, "
        "noting that real institutional datasets may exhibit higher missingness than synthetic data."
    )

    print(
        "\nClass imbalance:\n"
        f"- The at-risk class proportion (performance_risk = 1) is approximately {at_risk_rate:.2f}%. "
        "This indicates an imbalanced classification setting in which accuracy alone is insufficient. "
        "Accordingly, macro-averaged F1-score and confusion matrix analysis are methodologically justified, "
        "and SMOTE may be applied on the training split to improve minority-class learning."
    )

    # A defensible interpretation of expected correlation structure
    if "cumulative_cgpa" in df.columns and "prev_semester_gpa" in df.columns:
        r_cgpa_gpa = float(df[["cumulative_cgpa", "prev_semester_gpa"]].corr().iloc[0, 1])
        print(
            "\nCorrelation patterns:\n"
            f"- The correlation between cumulative CGPA and previous semester GPA is r = {r_cgpa_gpa:.3f}. "
            "A positive association is expected because both variables measure related aspects of academic achievement. "
            "Such overlap should be interpreted as shared measurement rather than evidence of causality."
        )
    else:
        print(
            "\nCorrelation patterns:\n"
            "- Correlation analysis of numeric predictors provides preliminary evidence of redundancy among variables. "
            "Where strong correlations occur, they may indicate overlapping constructs rather than independent predictors."
        )

    print(
        "\nInterpretive caution:\n"
        "- EDA findings are descriptive and should not be interpreted as causal relationships. "
        "Inferences about determinants of performance require stronger study designs beyond predictive modeling."
    )


if __name__ == "__main__":
    main()
