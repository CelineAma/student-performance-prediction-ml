from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    roc_auc_score,
    roc_curve,
)


@dataclass
class EvaluationResult:
    metrics: Dict[str, Any]
    classification_report_text: str


def evaluate_classifier(
    y_true,
    y_pred,
    y_proba: Optional[np.ndarray] = None,
) -> EvaluationResult:
    metrics: Dict[str, Any] = {}

    metrics["accuracy"] = float(accuracy_score(y_true, y_pred))
    metrics["f1_macro"] = float(f1_score(y_true, y_pred, average="macro"))
    metrics["f1_weighted"] = float(f1_score(y_true, y_pred, average="weighted"))

    report = classification_report(y_true, y_pred)

    if y_proba is not None:
        # Binary ROC-AUC only (simple and commonly expected in undergraduate reports)
        if y_proba.ndim == 1:
            proba_pos = y_proba
        elif y_proba.shape[1] == 2:
            proba_pos = y_proba[:, 1]
        else:
            proba_pos = None

        if proba_pos is not None:
            try:
                metrics["roc_auc"] = float(roc_auc_score(y_true, proba_pos))
            except Exception:
                pass

    return EvaluationResult(metrics=metrics, classification_report_text=report)


def save_metrics(result: EvaluationResult, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "metrics": result.metrics,
        "classification_report": result.classification_report_text,
    }
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def save_confusion_matrix(y_true, y_pred, out_path: Path, title: str) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    cm = confusion_matrix(y_true, y_pred)
    fig = plt.figure(figsize=(6, 5))
    plt.imshow(cm, interpolation="nearest")
    plt.title(title)
    plt.colorbar()
    plt.xlabel("Predicted")
    plt.ylabel("True")

    thresh = cm.max() / 2.0 if cm.size else 0
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(
                j,
                i,
                format(cm[i, j], "d"),
                ha="center",
                va="center",
                color="white" if cm[i, j] > thresh else "black",
            )

    plt.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def save_roc_curve(y_true, proba_pos: np.ndarray, out_path: Path, title: str) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fpr, tpr, _ = roc_curve(y_true, proba_pos)
    fig = plt.figure(figsize=(6, 5))
    plt.plot(fpr, tpr, label="ROC")
    plt.plot([0, 1], [0, 1], linestyle="--", label="Chance")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
