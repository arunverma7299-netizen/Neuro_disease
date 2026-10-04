from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from config import FEATURE_NOTES, PROCESSED_DATA_DIR, RAW_DATA_PATH, REPORTS_DIR, TARGET_COLUMN


def load_dataset(input_path: Path) -> pd.DataFrame:
    processed_path = PROCESSED_DATA_DIR / "neuropulse_cleaned.csv"
    if processed_path.exists():
        return pd.read_csv(processed_path)
    if not input_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {input_path}. Run 01_data_preparation.py after copying the CSV into backend/ml/data/raw."
        )
    return pd.read_csv(input_path)


def build_eda_report(df: pd.DataFrame) -> dict[str, object]:
    missing_by_column = df.isna().sum().to_dict()
    categorical_columns = [
        column_name for column_name in df.columns if not pd.api.types.is_numeric_dtype(df[column_name])
    ]
    numerical_columns = [
        column_name for column_name in df.columns if pd.api.types.is_numeric_dtype(df[column_name])
    ]

    return {
        "dataset_shape": [int(df.shape[0]), int(df.shape[1])],
        "missing_values_by_column": missing_by_column,
        "categorical_columns": categorical_columns,
        "numerical_columns": numerical_columns,
        "target_distribution": df[TARGET_COLUMN].value_counts().to_dict(),
        "feature_notes": FEATURE_NOTES,
        "column_list": list(df.columns),
    }


def write_markdown_report(report: dict[str, object]) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / "phase1_eda_report.md"

    lines: list[str] = []
    lines.append("# NeuroPulse Phase 1 EDA Report")
    lines.append("")
    lines.append("## Dataset Overview")
    lines.append(f"- Shape: {report['dataset_shape'][0]} rows x {report['dataset_shape'][1]} columns")
    lines.append("")
    lines.append("## Missing Values")
    for column_name, missing_count in report["missing_values_by_column"].items():
        lines.append(f"- {column_name}: {missing_count}")
    lines.append("")
    lines.append("## Column Types")
    lines.append("### Categorical")
    for column_name in report["categorical_columns"]:
        lines.append(f"- {column_name}")
    lines.append("")
    lines.append("### Numerical")
    for column_name in report["numerical_columns"]:
        lines.append(f"- {column_name}")
    lines.append("")
    lines.append("## Target Distribution")
    for label_name, count in report["target_distribution"].items():
        lines.append(f"- {label_name}: {count}")
    lines.append("")
    lines.append("## Feature Notes")
    for column_name, note in report["feature_notes"].items():
        lines.append(f"- {column_name}: {note}")
    lines.append("")
    lines.append("## Modeling Notes")
    lines.append("- The provided Target column is already a suitable educational label.")
    lines.append("- Burnout_Risk_Pct is kept as a reference score and not used as an input feature.")
    lines.append("- The first model frame uses only the 10 core scan features aligned with the intended NeuroScan flow.")

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the NeuroPulse Phase 1 EDA report.")
    parser.add_argument("--input", type=Path, default=RAW_DATA_PATH, help="Path to the raw CSV file.")
    args = parser.parse_args()

    df = load_dataset(args.input)
    report = build_eda_report(df)
    report_path = write_markdown_report(report)

    json_path = REPORTS_DIR / "phase1_eda_summary.json"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"Saved EDA report to: {report_path}")
    print(f"Saved EDA summary to: {json_path}")


if __name__ == "__main__":
    main()
