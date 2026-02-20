from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


@dataclass
class PreprocessingSpec:
    numeric_features: List[str]
    categorical_features: List[str]


def infer_feature_types(df: pd.DataFrame, target: str) -> PreprocessingSpec:
    """Infer numeric/categorical feature lists from a DataFrame.

    Academic note:
    - Automatic inference is convenient for a boilerplate.
    - For the final report, you should justify any manual overrides you apply.
    """

    X = df.drop(columns=[target])

    numeric_features = X.select_dtypes(include=["number", "bool"]).columns.tolist()
    categorical_features = [c for c in X.columns if c not in numeric_features]

    return PreprocessingSpec(
        numeric_features=numeric_features,
        categorical_features=categorical_features,
    )


def build_preprocessor(spec: PreprocessingSpec) -> ColumnTransformer:
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "onehot",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
            ),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, spec.numeric_features),
            ("cat", categorical_pipeline, spec.categorical_features),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )

    return preprocessor


def get_feature_names(preprocessor: ColumnTransformer) -> List[str]:
    """Return output feature names after preprocessing."""

    try:
        names = preprocessor.get_feature_names_out().tolist()
    except Exception:
        names = []
    return names


def split_train_test(
    df: pd.DataFrame,
    target: str,
    test_size: float = 0.2,
    random_state: int = 42,
    stratify: bool = True,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Split a dataset into train and test partitions.

    Parameters
    - df: input DataFrame containing features and target.
    - target: target column name.
    - test_size: proportion of data reserved for testing.
    - random_state: random seed for reproducibility.
    - stratify: if True, stratify by the target when it has more than one class.

    Returns
    - X_train, X_test, y_train, y_test
    """

    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found in dataset columns.")

    X = df.drop(columns=[target])
    y = df[target]

    strat = y if (stratify and y.nunique() > 1) else None
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=strat,
    )

    return X_train, X_test, y_train, y_test


def build_preprocessor_from_dataframe(df: pd.DataFrame, target: str) -> ColumnTransformer:
    """Convenience wrapper to infer feature types and build a preprocessor.

    This is useful when you want a single, readable entry point for:
    - identifying numeric vs categorical predictors;
    - handling missing values (median for numeric, mode for categorical);
    - encoding categorical variables (one-hot);
    - scaling numeric variables (standard scaling).
    """

    spec = infer_feature_types(df=df, target=target)
    return build_preprocessor(spec)
