from __future__ import annotations

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    service: str


class FactorImpact(BaseModel):
    feature: str
    value: float | int
    impact: str


class PredictionResponse(BaseModel):
    score: int = Field(ge=0, le=100)
    state: str
    confidence: float = Field(ge=0, le=1)
    top_factors: list[FactorImpact] = Field(default_factory=list)
    decision_path: list[str] = Field(default_factory=list)
    model_version: str = "v0.1.0"
    message: str | None = None


class HistoryEntryResponse(BaseModel):
    id: int
    created_at: str
    score: int
    state: str
    sleep_hours: float
    screen_time: float
    exercise_minutes: int
    stress_level: int
    model_version: str


class HistoryResponse(BaseModel):
    entries: list[HistoryEntryResponse]


class ModelInfoResponse(BaseModel):
    model_name: str
    model_version: str
    status: str
    description: str
    best_model: str | None = None
    metrics: dict[str, float] = Field(default_factory=dict)
    feature_names: list[str] = Field(default_factory=list)


class FeedbackResponse(BaseModel):
    received: bool
    message: str

