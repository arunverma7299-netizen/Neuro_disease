from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from config import (
    ALL_ANALYSIS_FEATURES,
    ARTIFACTS_DIR,
    CORE_MODEL_FEATURES,
    EXPECTED_RANGES,
    FEATURE_NOTES,
    LEAKAGE_COLUMNS,
    PROCESSED_DATA_DIR,
    RAW_DATA_PATH,
    REPORTS_DIR,
    SCORE_COLUMN,
    TARGET_COLUMN,
    TARGET_ORDER,
    TARGET_SCORE_CENTERS,
    TARGET_UI_SCORE_BANDS,
    USER_ID_COLUMN,
)


@dataclass(frozen=True)
class DataPrepSummary:
    rows: int
    columns: int
    duplicate_rows: int
    missing_values: int
    categorical_columns: list[str]
    numerical_columns: list[str]
    core_features: list[str]
    target_counts: dict[str, int]
    score_by_target: dict[str, dict[str, float]]
    quality_issues: dict[str, int]


def load_dataset(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {path}. Copy neuropulse_dataset.csv into backend/ml/data/raw first."
        )
    return pd.read_csv(path)


def validate_required_columns(df: pd.DataFrame) -> None:
    required_columns = {USER_ID_COLUMN, TARGET_COLUMN, SCORE_COLUMN, *CORE_MODEL_FEATURES}
    missing_columns = sorted(required_columns - set(df.columns))
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")


def build_quality_issues(df: pd.DataFrame) -> dict[str, int]:
    issues: dict[str, int] = {}
    for column_name, (lower_bound, upper_bound) in EXPECTED_RANGES.items():
        if column_name in df.columns:
            mask = df[column_name].lt(lower_bound) | df[column_name].gt(upper_bound)
            issues[column_name] = int(mask.sum())
    return issues


def profile_dataset(df: pd.DataFrame) -> DataPrepSummary:
    feature_frame = df.drop(columns=[USER_ID_COLUMN, TARGET_COLUMN], errors="ignore")
    categorical_columns = [
        column_name
        for column_name in feature_frame.columns
        if not pd.api.types.is_numeric_dtype(feature_frame[column_name])
    ]
    numerical_columns = [
        column_name
        for column_name in feature_frame.columns
        if pd.api.types.is_numeric_dtype(feature_frame[column_name])
    ]
    score_summary = (
        df.groupby(TARGET_COLUMN)[SCORE_COLUMN]
        .agg(["min", "mean", "max"])
        .round(2)
        .to_dict(orient="index")
    )

    return DataPrepSummary(
        rows=int(df.shape[0]),
        columns=int(df.shape[1]),
        duplicate_rows=int(df.duplicated().sum()),
        missing_values=int(df.isna().sum().sum()),
        categorical_columns=categorical_columns,
        numerical_columns=numerical_columns,
        core_features=CORE_MODEL_FEATURES,
        target_counts=df[TARGET_COLUMN].value_counts().reindex(TARGET_ORDER).fillna(0).astype(int).to_dict(),
        score_by_target=score_summary,
        quality_issues=build_quality_issues(df),
    )


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned.columns = [column_name.strip() for column_name in cleaned.columns]
    cleaned = cleaned.drop_duplicates().reset_index(drop=True)
    return cleaned


def build_report(df: pd.DataFrame, summary: DataPrepSummary) -> dict[str, object]:
    return {
        "dataset_path": str(RAW_DATA_PATH),
        "rows": summary.rows,
        "columns": summary.columns,
        "missing_values": summary.missing_values,
        "duplicate_rows": summary.duplicate_rows,
        "categorical_columns": summary.categorical_columns,
        "numerical_columns": summary.numerical_columns,
        "feature_notes": FEATURE_NOTES,
        "core_model_features": summary.core_features,
        "leakage_columns_excluded_from_training": LEAKAGE_COLUMNS,
        "target_order": TARGET_ORDER,
        "target_ui_score_bands": TARGET_UI_SCORE_BANDS,
        "target_score_centers": TARGET_SCORE_CENTERS,
        "target_counts": summary.target_counts,
        "score_by_target": summary.score_by_target,
        "quality_issues": summary.quality_issues,
        "used_training_features": CORE_MODEL_FEATURES,
        "excluded_features": [
            column_name
            for column_name in ALL_ANALYSIS_FEATURES
            if column_name not in CORE_MODEL_FEATURES and column_name != SCORE_COLUMN
        ],
        "notes": [
            "The provided Target column is treated as the educational class label.",
            "Burnout_Risk_Pct is preserved as a reference score and not used as a training feature.",
            "Additional columns are documented for transparency and future analysis.",
        ],
    }


def save_outputs(cleaned_df: pd.DataFrame, report: dict[str, object]) -> None:
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    cleaned_path = PROCESSED_DATA_DIR / "neuropulse_cleaned.csv"
    model_frame_path = PROCESSED_DATA_DIR / "neuropulse_model_frame.csv"
    report_path = REPORTS_DIR / "phase1_data_profile.json"

    cleaned_df.to_csv(cleaned_path, index=False)
    cleaned_df[CORE_MODEL_FEATURES + [TARGET_COLUMN]].to_csv(model_frame_path, index=False)

    with report_path.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)

    print(f"Saved cleaned dataset to: {cleaned_path}")
    print(f"Saved model frame to: {model_frame_path}")
    print(f"Saved profile report to: {report_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare the NeuroPulse dataset for Phase 1.")
    parser.add_argument("--input", type=Path, default=RAW_DATA_PATH, help="Path to the raw CSV file.")
    args = parser.parse_args()

    raw_df = load_dataset(args.input)
    validate_required_columns(raw_df)
    cleaned_df = clean_dataset(raw_df)
    summary = profile_dataset(cleaned_df)
    report = build_report(cleaned_df, summary)
    save_outputs(cleaned_df, report)


if __name__ == "__main__":
    main()
