from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import shap


def _pick_class_index(shap_values) -> Optional[int]:
    # shap_values can be:
    # - array (n_samples, n_features) for regression/binary
    # - list of arrays for multiclass
    if isinstance(shap_values, list):
        if len(shap_values) == 2:
            return 1
        return int(np.argmax([np.mean(np.abs(sv)) for sv in shap_values]))
    # Some versions/models return a 3D array for classification.
    # For binary classification, we select the positive class (index 1).
    try:
        arr = np.asarray(shap_values)
        if arr.ndim == 3 and (2 in arr.shape):
            return 1
    except Exception:
        pass
    return None


def shap_summary_plot_for_pipeline(
    pipeline: Any,
    X,
    out_path: Path,
    max_display: int = 20,
    title: str = "SHAP Summary",
) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    preprocessor = pipeline.named_steps.get("preprocessor")
    model = pipeline.named_steps.get("model")

    X_trans = preprocessor.transform(X)
    feature_names = None
    try:
        feature_names = preprocessor.get_feature_names_out()
    except Exception:
        feature_names = None

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_trans)

    class_idx = _pick_class_index(shap_values)

    plt.figure(figsize=(10, 6))
    if class_idx is None:
        shap.summary_plot(
            shap_values,
            X_trans,
            feature_names=feature_names,
            max_display=max_display,
            show=False,
        )
    else:
        shap_values = _extract_shap_for_class(shap_values, class_idx)
        shap.summary_plot(
            shap_values,
            X_trans,
            feature_names=feature_names,
            max_display=max_display,
            show=False,
        )

    plt.title(title)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def _extract_shap_for_class(shap_values, class_idx: Optional[int]):
    """Return SHAP values for a single class when needed.

    Handles common shapes:
    - list[n_classes] of (n_samples, n_features)
    - (n_samples, n_features)
    - (n_samples, n_features, n_classes)
    - (n_samples, n_classes, n_features)
    """

    if isinstance(shap_values, list):
        if class_idx is None:
            return shap_values
        return shap_values[class_idx]

    arr = np.asarray(shap_values)
    if arr.ndim == 2:
        return arr

    if arr.ndim == 3 and class_idx is not None:
        # Most common: (n_samples, n_features, n_classes)
        if arr.shape[-1] > 1:
            return arr[:, :, class_idx]
        # Alternate: (n_samples, n_classes, n_features)
        if arr.shape[1] > 1:
            return arr[:, class_idx, :]

    return arr


def shap_local_waterfall_for_pipeline(
    pipeline: Any,
    X,
    instance_index: int,
    out_path: Path,
    max_display: int = 15,
    title: str = "SHAP Local Explanation",
) -> Dict[str, Any]:
    """Generate a local SHAP explanation for a single row.

    Returns a small dictionary containing:
    - instance_index
    - predicted_label (if available)
    - top_positive and top_negative contributions
    """

    out_path.parent.mkdir(parents=True, exist_ok=True)

    preprocessor = pipeline.named_steps.get("preprocessor")
    model = pipeline.named_steps.get("model")

    X_trans = preprocessor.transform(X)
    try:
        feature_names = preprocessor.get_feature_names_out().tolist()
    except Exception:
        feature_names = [f"feature_{i}" for i in range(int(X_trans.shape[1]))]

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_trans)
    class_idx = _pick_class_index(shap_values)
    shap_mat = _extract_shap_for_class(shap_values, class_idx)

    # base value can be scalar, array, or list depending on estimator/task
    base_values = getattr(explainer, "expected_value", 0.0)
    if isinstance(base_values, list) and class_idx is not None:
        base_value = base_values[class_idx]
    elif isinstance(base_values, np.ndarray) and base_values.ndim == 1 and class_idx is not None:
        base_value = base_values[class_idx]
    else:
        base_value = base_values

    idx = int(instance_index)
    row_values = np.asarray(shap_mat)[idx]
    if row_values.ndim != 1:
        # Defensive handling for unexpected shapes.
        # If a class dimension remains, select the positive class.
        if row_values.ndim == 2 and row_values.shape[-1] == 2:
            row_values = row_values[:, 1]
        elif row_values.ndim == 2 and row_values.shape[0] == 2:
            row_values = row_values[1, :]
        row_values = np.asarray(row_values).reshape(-1)
    row_data = np.asarray(X_trans)[idx]

    explanation = shap.Explanation(
        values=row_values,
        base_values=base_value,
        data=row_data,
        feature_names=feature_names,
    )

    plt.figure(figsize=(10, 6))
    shap.plots.waterfall(explanation, max_display=max_display, show=False)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()

    contributions = pd_series_from_shap(row_values, feature_names)
    top_positive = contributions[contributions > 0].sort_values(ascending=False).head(8)
    top_negative = contributions[contributions < 0].sort_values(ascending=True).head(8)

    predicted_label = None
    try:
        predicted_label = int(pipeline.predict(X.iloc[[idx]] if hasattr(X, "iloc") else X[idx : idx + 1])[0])
    except Exception:
        predicted_label = None

    return {
        "instance_index": idx,
        "predicted_label": predicted_label,
        "top_positive": top_positive.to_dict(),
        "top_negative": top_negative.to_dict(),
    }


def pd_series_from_shap(values: np.ndarray, feature_names: List[str]):
    # Local import to avoid adding pandas as a hard dependency in module import order.
    import pandas as pd

    return pd.Series(values, index=feature_names, dtype=float)
