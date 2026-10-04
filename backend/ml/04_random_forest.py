from __future__ import annotations

import argparse

from sklearn.ensemble import RandomForestClassifier

from config import REPORTS_DIR, TARGET_ORDER
from training_utils import (
    artifact_dir,
    build_pipeline,
    evaluate_model,
    load_training_frame,
    save_confusion_matrix_plot,
    save_json,
    save_model,
    split_data,
    timed_fit,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Train the NeuroPulse Random Forest baseline.")
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args()

    frame = load_training_frame()
    split = split_data(frame, random_state=args.random_state)

    pipeline = build_pipeline(
        RandomForestClassifier(
            n_estimators=200,
            random_state=args.random_state,
            class_weight="balanced",
            n_jobs=-1,
        )
    )
    fitted_model, training_seconds = timed_fit(pipeline, split.x_train, split.y_train)
    metrics = evaluate_model(fitted_model, split.x_test, split.y_test)

    artifact_path = artifact_dir() / "random_forest_baseline.joblib"
    save_model(artifact_path, fitted_model)

    save_json(
        REPORTS_DIR / "random_forest_baseline.json",
        {
            "model_name": "Random Forest",
            "training_seconds": training_seconds,
            "metrics": metrics,
        },
    )
    save_confusion_matrix_plot(
        REPORTS_DIR / "random_forest_confusion_matrix.png",
        metrics["confusion_matrix"],
        TARGET_ORDER,
        "Random Forest Confusion Matrix",
    )

    print(f"Saved Random Forest baseline to: {artifact_path}")
    print(f"Accuracy: {metrics['accuracy']:.4f}, F1: {metrics['f1_macro']:.4f}")


if __name__ == "__main__":
    main()
