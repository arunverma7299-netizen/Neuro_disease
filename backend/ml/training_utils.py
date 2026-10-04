from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from config import ARTIFACTS_DIR, CORE_MODEL_FEATURES, PROCESSED_DATA_DIR, REPORTS_DIR, TARGET_COLUMN


@dataclass(frozen=True)
class SplitData:
    x_train: pd.DataFrame
    x_test: pd.DataFrame
    y_train: pd.Series
    y_test: pd.Series


def load_training_frame() -> pd.DataFrame:
    frame_path = PROCESSED_DATA_DIR / "neuropulse_model_frame.csv"
    if not frame_path.exists():
        raise FileNotFoundError(
            f"Missing processed model frame: {frame_path}. Run backend/ml/01_data_preparation.py first."
        )
    return pd.read_csv(frame_path)


def prepare_features_and_target(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    missing_columns = [column_name for column_name in CORE_MODEL_FEATURES + [TARGET_COLUMN] if column_name not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing expected columns in model frame: {missing_columns}")

    x = df[CORE_MODEL_FEATURES].copy()
    y = df[TARGET_COLUMN].copy()
    return x, y


def split_data(df: pd.DataFrame, random_state: int = 42, test_size: float = 0.2) -> SplitData:
    x, y = prepare_features_and_target(df)
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )
    return SplitData(x_train=x_train, x_test=x_test, y_train=y_train, y_test=y_test)


def build_pipeline(estimator) -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", SimpleImputer(strategy="median"), CORE_MODEL_FEATURES),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )
    return Pipeline([("preprocess", preprocessor), ("model", estimator)])


def evaluate_model(model, x_test: pd.DataFrame, y_test: pd.Series) -> dict[str, object]:
    y_pred = model.predict(x_test)
    if hasattr(model, "predict_proba"):
        y_proba = model.predict_proba(x_test)
    else:
        y_proba = None

    return {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision_macro": float(precision_score(y_test, y_pred, average="macro", zero_division=0)),
        "recall_macro": float(recall_score(y_test, y_pred, average="macro", zero_division=0)),
        "f1_macro": float(f1_score(y_test, y_pred, average="macro", zero_division=0)),
        "classification_report": classification_report(y_test, y_pred, zero_division=0, output_dict=True),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        "predictions": y_pred.tolist(),
        "probabilities": y_proba.tolist() if y_proba is not None else None,
    }


def timed_fit(model, x_train: pd.DataFrame, y_train: pd.Series) -> tuple[object, float]:
    start = perf_counter()
    model.fit(x_train, y_train)
    end = perf_counter()
    return model, end - start


def save_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


def save_model(path: Path, model: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)


def save_confusion_matrix_plot(path: Path, matrix: list[list[int]], labels: list[str], title: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    image = ax.imshow(matrix, cmap="Blues")
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=20, ha="right")
    ax.set_yticklabels(labels)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title(title)

    for row_index, row in enumerate(matrix):
        for column_index, value in enumerate(row):
            ax.text(column_index, row_index, str(value), ha="center", va="center", color="black")

    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def score_mapping() -> dict[str, int]:
    return {
        "Calm": 15,
        "Balanced": 40,
        "Strained": 60,
        "Overloaded": 85,
    }


def plot_dir() -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    return REPORTS_DIR


def artifact_dir() -> Path:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    return ARTIFACTS_DIR

