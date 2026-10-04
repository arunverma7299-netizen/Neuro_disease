from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import joblib
from fastapi import HTTPException

from app.schemas.requests import PredictionRequest, SimulationRequest
from app.schemas.responses import FactorImpact, ModelInfoResponse, PredictionResponse


PROJECT_ROOT = Path(__file__).resolve().parents[3]
ML_ROOT = PROJECT_ROOT / "backend" / "ml"
ARTIFACTS_DIR = ML_ROOT / "artifacts"
MODEL_PATH = ARTIFACTS_DIR / "best_model.joblib"
MODEL_METADATA_PATH = ARTIFACTS_DIR / "best_model_metadata.json"
EXPLAINER_MODEL_PATH = ARTIFACTS_DIR / "decision_tree_tuned.joblib"
PHASE1_PROFILE_PATH = ML_ROOT / "reports" / "phase1_data_profile.json"


@lru_cache(maxsize=1)
def load_model_bundle() -> dict[str, object]:
    if not MODEL_PATH.exists() or not MODEL_METADATA_PATH.exists():
        return {"status": "unavailable"}

    model = joblib.load(MODEL_PATH)
    metadata = json.loads(MODEL_METADATA_PATH.read_text(encoding="utf-8"))
    explainer = joblib.load(EXPLAINER_MODEL_PATH) if EXPLAINER_MODEL_PATH.exists() else None
    return {"status": "ready", "model": model, "metadata": metadata, "explainer": explainer}


def _unavailable_prediction_message() -> HTTPException:
    return HTTPException(
        status_code=503,
        detail=(
            "The trained model artifact is not available yet. "
            "Run the ML training phase and save backend/ml/artifacts/best_model.joblib first."
        ),
    )


def _feature_factors(payload: PredictionRequest) -> list[FactorImpact]:
    return [
        FactorImpact(feature="sleep_hours", value=payload.sleep_hours, impact="contextual"),
        FactorImpact(feature="screen_time", value=payload.screen_time, impact="contextual"),
        FactorImpact(feature="exercise_minutes", value=payload.exercise_minutes, impact="contextual"),
        FactorImpact(feature="stress_level", value=payload.stress_level, impact="contextual"),
        FactorImpact(feature="resting_heart_rate", value=payload.resting_heart_rate, impact="contextual"),
    ]


def _extract_classes(model: object) -> list[object]:
    classes = getattr(model, "classes_", None)
    if classes is not None:
        return list(classes)

    named_steps = getattr(model, "named_steps", None)
    if named_steps:
        last_step_name = list(named_steps.keys())[-1]
        last_step = named_steps[last_step_name]
        step_classes = getattr(last_step, "classes_", None)
        if step_classes is not None:
            return list(step_classes)

    return []


def predict_scan(payload: PredictionRequest) -> PredictionResponse:
    bundle = load_model_bundle()
    if bundle["status"] != "ready":
        raise _unavailable_prediction_message()

    model = bundle["model"]
    metadata = bundle["metadata"]
    import pandas as pd

    feature_row = pd.DataFrame(
        [
            {
                "Sleep_Hours": payload.sleep_hours,
                "Sleep_Quality": payload.sleep_quality,
                "Screen_Time_Hours": payload.screen_time,
                "Work_Study_Hours": payload.work_hours,
                "Exercise_Minutes": payload.exercise_minutes,
                "Caffeine_Cups": payload.caffeine,
                "Water_Liters": payload.water_intake,
                "Stress_Level": payload.stress_level,
                "Social_Interaction_Hours": payload.social_activity,
                "Resting_Heart_Rate": payload.resting_heart_rate,
            }
        ]
    )

    predicted_state = model.predict(feature_row)[0]
    predicted_probabilities = model.predict_proba(feature_row)[0]
    classes = _extract_classes(model)
    if not classes:
        raise HTTPException(status_code=500, detail="The saved model does not expose class labels.")

    state_index = classes.index(predicted_state)
    confidence = float(predicted_probabilities[state_index])
    score = int(round(metadata.get("score_mapping", {}).get(predicted_state, 50)))
    explainer = bundle.get("explainer")
    decision_path = metadata.get("decision_path_template", [])
    if explainer is not None and hasattr(explainer, "named_steps"):
        try:
            decision_path = _build_decision_path(explainer, feature_row, metadata.get("decision_path_template", []))
        except Exception:
            decision_path = metadata.get("decision_path_template", [])

    return PredictionResponse(
        score=score,
        state=str(predicted_state),
        confidence=confidence,
        top_factors=_feature_factors(payload),
        decision_path=decision_path,
        model_version=str(metadata.get("model_version", "v0.1.0")),
        message="Prediction generated from the trained NeuroPulse model.",
    )


def _build_decision_path(explainer: object, feature_row, fallback_template: list[str]) -> list[str]:
    feature_names = [
        "Sleep_Hours",
        "Sleep_Quality",
        "Screen_Time_Hours",
        "Work_Study_Hours",
        "Exercise_Minutes",
        "Caffeine_Cups",
        "Water_Liters",
        "Stress_Level",
        "Social_Interaction_Hours",
        "Resting_Heart_Rate",
    ]
    transformed_row = explainer.named_steps["preprocess"].transform(feature_row)
    tree = explainer.named_steps["model"]
    node_indicator = tree.decision_path(transformed_row)
    feature = tree.tree_.feature
    threshold = tree.tree_.threshold
    sample_index = 0
    node_index = node_indicator.indices[node_indicator.indptr[sample_index] : node_indicator.indptr[sample_index + 1]]
    steps: list[str] = []
    transformed_values = transformed_row[0]
    for node_id in node_index:
        if feature[node_id] == -2:
            continue
        feature_name = feature_names[feature[node_id]]
        comparison_value = float(transformed_values[feature[node_id]])
        if comparison_value <= threshold[node_id]:
            step = f"{feature_name}: {comparison_value:.1f} is at or below {threshold[node_id]:.1f}"
        else:
            step = f"{feature_name}: {comparison_value:.1f} is above {threshold[node_id]:.1f}"
        if not steps or steps[-1] != step:
            steps.append(step)
        if len(steps) >= 3:
            break
    return steps or list(fallback_template)


def simulate_scan(payload: SimulationRequest) -> PredictionResponse:
    return predict_scan(payload)


def get_model_info() -> ModelInfoResponse:
    profile = {}
    if PHASE1_PROFILE_PATH.exists():
        profile = json.loads(PHASE1_PROFILE_PATH.read_text(encoding="utf-8"))

    bundle = load_model_bundle()
    if bundle["status"] != "ready":
        return ModelInfoResponse(
            model_name="NeuroPulse classifier",
            model_version="v0.1.0",
            status="not_trained",
            description="The backend contract is ready, but the trained model artifact has not been saved yet.",
            best_model=None,
            metrics={},
            feature_names=profile.get("used_training_features", []),
        )

    metadata = bundle["metadata"]
    return ModelInfoResponse(
        model_name="NeuroPulse classifier",
        model_version=str(metadata.get("model_version", "v0.1.0")),
        status="ready",
        description="Trained educational classifier for lifestyle-based mental-load estimation.",
        best_model=str(metadata.get("best_model", "Decision Tree")),
        metrics=metadata.get("metrics", {}),
        feature_names=metadata.get("feature_names", profile.get("used_training_features", [])),
    )

