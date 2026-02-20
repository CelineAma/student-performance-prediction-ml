from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Tuple

import numpy as np
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.ensemble import RandomForestClassifier

try:
    from lightgbm import LGBMClassifier
except Exception:  # pragma: no cover
    LGBMClassifier = None


@dataclass
class ModelSpec:
    name: str
    pipeline: Any


def build_random_forest_pipeline(preprocessor, random_state: int) -> ModelSpec:
    clf = RandomForestClassifier(
        n_estimators=400,
        random_state=random_state,
        n_jobs=-1,
        class_weight=None,
    )

    pipe = ImbPipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("smote", SMOTE(random_state=random_state)),
            ("model", clf),
        ]
    )

    return ModelSpec(name="random_forest", pipeline=pipe)


def build_lightgbm_pipeline(preprocessor, random_state: int) -> ModelSpec:
    if LGBMClassifier is None:
        raise ImportError("lightgbm is not installed. Install it to train LightGBM.")

    clf = LGBMClassifier(
        n_estimators=800,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        random_state=random_state,
        n_jobs=-1,
    )

    pipe = ImbPipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("smote", SMOTE(random_state=random_state)),
            ("model", clf),
        ]
    )

    return ModelSpec(name="lightgbm", pipeline=pipe)
