from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

from app.schemas.responses import PredictionResponse


class PredictionRequest(BaseModel):
    sleep_hours: float = Field(ge=0, le=24)
    sleep_quality: int = Field(ge=1, le=10)
    screen_time: float = Field(ge=0, le=24)
    work_hours: float = Field(ge=0, le=24)
    exercise_minutes: int = Field(ge=0, le=600)
    caffeine: int = Field(ge=0, le=20)
    water_intake: float = Field(ge=0, le=10)
    stress_level: int = Field(ge=1, le=10)
    social_activity: float = Field(ge=0, le=24)
    resting_heart_rate: int = Field(ge=30, le=200)

    @field_validator("sleep_hours", "screen_time", "work_hours", "water_intake", "social_activity")
    @classmethod
    def round_to_one_decimal(cls, value: float) -> float:
        return round(float(value), 1)


class SimulationRequest(PredictionRequest):
    pass


class HistoryCreateRequest(BaseModel):
    score: int = Field(ge=0, le=100)
    state: str
    sleep_hours: float = Field(ge=0, le=24)
    screen_time: float = Field(ge=0, le=24)
    exercise_minutes: int = Field(ge=0, le=600)
    stress_level: int = Field(ge=1, le=10)
    model_version: str = "v0.1.0"

    @classmethod
    def from_prediction(cls, payload: PredictionRequest, prediction: PredictionResponse) -> "HistoryCreateRequest":
        return cls(
            score=prediction.score,
            state=prediction.state,
            sleep_hours=payload.sleep_hours,
            screen_time=payload.screen_time,
            exercise_minutes=payload.exercise_minutes,
            stress_level=payload.stress_level,
            model_version=prediction.model_version,
        )


class FeedbackRequest(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str | None = None

