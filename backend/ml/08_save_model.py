from __future__ import annotations

import argparse
import json

import joblib

from config import ARTIFACTS_DIR, CORE_MODEL_FEATURES, REPORTS_DIR, TARGET_ORDER


def main() -> None:
    parser = argparse.ArgumentParser(description="Save the selected NeuroPulse model artifact and metadata.")
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args()

    metrics_path = REPORTS_DIR / "best_model_metrics.json"
    if not metrics_path.exists():
        raise FileNotFoundError("Missing best_model_metrics.json. Run 07_model_evaluation.py first.")

    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    best_model_name = metrics["best_model"]
    best_model_path = ARTIFACTS_DIR / f"{best_model_name}_tuned.joblib"
    if not best_model_path.exists():
        raise FileNotFoundError(f"Missing tuned model artifact: {best_model_path}")

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    model = joblib.load(best_model_path)
    joblib.dump(model, ARTIFACTS_DIR / "best_model.joblib")

    metadata = {
        "model_version": "v1.0.0",
        "best_model": best_model_name,
        "metrics": metrics["metrics"],
        "feature_names": CORE_MODEL_FEATURES,
        "class_labels": TARGET_ORDER,
        "score_mapping": {
            "Calm": 15,
            "Balanced": 40,
            "Strained": 60,
            "Overloaded": 85,
        },
        "decision_path_template": [
            "Sleep duration and screen exposure were compared against the learned thresholds.",
            "Stress level and recovery-related signals were evaluated together.",
            "The model combined the strongest contributing lifestyle features to produce the final state.",
        ],
    }
    (ARTIFACTS_DIR / "best_model_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print(f"Saved best model to: {ARTIFACTS_DIR / 'best_model.joblib'}")
    print(f"Saved metadata to: {ARTIFACTS_DIR / 'best_model_metadata.json'}")


if __name__ == "__main__":
    main()
