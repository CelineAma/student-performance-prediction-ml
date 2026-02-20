from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


@dataclass
class BasicFeatureEngineer(BaseEstimator, TransformerMixin):
    """Minimal, dataset-agnostic feature engineering.

    This transformer adds simple row-level features that are defensible in an
    academic setting without requiring domain-specific assumptions:

    - missing_count: number of missing values across input columns

    Notes:
    - Implemented for pandas DataFrame inputs (recommended for readability).
    - If a numpy array is provided, it is returned unchanged.
    """

    add_missing_count: bool = True

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if isinstance(X, pd.DataFrame):
            X_out = X.copy()
            if self.add_missing_count:
                X_out["missing_count"] = X_out.isna().sum(axis=1).astype(np.int64)
            return X_out

        return X
