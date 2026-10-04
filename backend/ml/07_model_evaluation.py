from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import pandas as pd

from config import ARTIFACTS_DIR, CORE_MODEL_FEATURES, REPORTS_DIR, TARGET_ORDER
from training_utils import evaluate_model, load_training_frame, save_confusion_matrix_plot, save_json, split_data


def load_tuned_model(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Missing tuned model artifact: {path}")
    return joblib.load(path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare tuned NeuroPulse models and select the best one.")
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args()

    frame = load_training_frame()
    split = split_data(frame, random_state=args.random_state)

    model_specs = {
        "decision_tree": ARTIFACTS_DIR / "decision_tree_tuned.joblib",
        "random_forest": ARTIFACTS_DIR / "random_forest_tuned.joblib",
        "extra_trees": ARTIFACTS_DIR / "extra_trees_tuned.joblib",
    }

    comparison_rows: list[dict[str, object]] = []
    tuned_models: dict[str, object] = {}
    for model_name, model_path in model_specs.items():
        if not model_path.exists():
            continue
        model = load_tuned_model(model_path)
        tuned_models[model_name] = model
        metrics = evaluate_model(model, split.x_test, split.y_test)
        comparison_rows.append(
            {
                "model": model_name,
                "accuracy": metrics["accuracy"],
                "precision_macro": metrics["precision_macro"],
                "recall_macro": metrics["recall_macro"],
                "f1_macro": metrics["f1_macro"],
            }
        )

    if not comparison_rows:
        raise FileNotFoundError("No tuned model artifacts were found. Run 06_hyperparameter_tuning.py first.")

    comparison_df = pd.DataFrame(comparison_rows).sort_values(["f1_macro", "accuracy"], ascending=False).reset_index(drop=True)
    best_row = comparison_df.iloc[0].to_dict()
    best_model_name = str(best_row["model"])

    save_json(
        REPORTS_DIR / "model_comparison.json",
        {
            "comparison": comparison_df.to_dict(orient="records"),
            "best_model": best_model_name,
            "feature_names": CORE_MODEL_FEATURES,
            "notes": [
                "The selected model is chosen by macro F1, then accuracy.",
                "Decision Tree remains available for explainability even when another model wins by a small margin.",
            ],
        },
    )
    comparison_df.to_csv(REPORTS_DIR / "model_comparison.csv", index=False)

    selected_model = tuned_models[best_model_name]
    selected_metrics = evaluate_model(selected_model, split.x_test, split.y_test)
    save_confusion_matrix_plot(
        REPORTS_DIR / f"{best_model_name}_confusion_matrix.png",
        selected_metrics["confusion_matrix"],
        TARGET_ORDER,
        f"{best_model_name.replace('_', ' ').title()} Confusion Matrix",
    )

    save_json(
        REPORTS_DIR / "best_model_metrics.json",
        {
            "best_model": best_model_name,
            "metrics": selected_metrics,
            "feature_names": CORE_MODEL_FEATURES,
        },
    )

    print(comparison_df.to_string(index=False))
    print(f"Best model: {best_model_name}")


if __name__ == "__main__":
    main()
