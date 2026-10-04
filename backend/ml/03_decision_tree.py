from __future__ import annotations

import argparse
from pathlib import Path

from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree

from config import CORE_MODEL_FEATURES, REPORTS_DIR, TARGET_ORDER
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
    parser = argparse.ArgumentParser(description="Train the NeuroPulse Decision Tree baseline.")
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args()

    frame = load_training_frame()
    split = split_data(frame, random_state=args.random_state)

    pipeline = build_pipeline(
        DecisionTreeClassifier(random_state=args.random_state, class_weight="balanced")
    )
    fitted_model, training_seconds = timed_fit(pipeline, split.x_train, split.y_train)
    metrics = evaluate_model(fitted_model, split.x_test, split.y_test)

    artifact_path = artifact_dir() / "decision_tree_baseline.joblib"
    save_model(artifact_path, fitted_model)

    save_json(
        REPORTS_DIR / "decision_tree_baseline.json",
        {
            "model_name": "Decision Tree",
            "training_seconds": training_seconds,
            "feature_names": CORE_MODEL_FEATURES,
            "metrics": metrics,
        },
    )
    save_confusion_matrix_plot(
        REPORTS_DIR / "decision_tree_confusion_matrix.png",
        metrics["confusion_matrix"],
        TARGET_ORDER,
        "Decision Tree Confusion Matrix",
    )

    tree = fitted_model.named_steps["model"]
    export_text_path = REPORTS_DIR / "decision_tree_rules.txt"
    export_text_path.write_text(
        export_text(tree, feature_names=CORE_MODEL_FEATURES, max_depth=4),
        encoding="utf-8",
    )

    fig_path = REPORTS_DIR / "decision_tree_plot.png"
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(18, 10))
    plot_tree(tree, feature_names=CORE_MODEL_FEATURES, class_names=TARGET_ORDER, filled=True, rounded=True, ax=ax, max_depth=3)
    fig.tight_layout()
    fig.savefig(fig_path, dpi=200, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved Decision Tree baseline to: {artifact_path}")
    print(f"Accuracy: {metrics['accuracy']:.4f}, F1: {metrics['f1_macro']:.4f}")


if __name__ == "__main__":
    main()
