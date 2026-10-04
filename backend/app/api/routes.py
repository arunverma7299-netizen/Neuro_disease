from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.requests import FeedbackRequest, HistoryCreateRequest, PredictionRequest, SimulationRequest
from app.schemas.responses import FeedbackResponse, HealthResponse, HistoryResponse, ModelInfoResponse, PredictionResponse
from app.services.history_service import create_history_entry, list_history_entries
from app.services.model_service import get_model_info, predict_scan, simulate_scan

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok", service="NeuroPulse API")


@router.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest, db: Session = Depends(get_db)) -> PredictionResponse:
    prediction = predict_scan(payload)
    create_history_entry(db=db, payload=HistoryCreateRequest.from_prediction(payload, prediction))
    return prediction


@router.post("/simulate", response_model=PredictionResponse)
def simulate(payload: SimulationRequest) -> PredictionResponse:
    return simulate_scan(payload)


@router.get("/history", response_model=HistoryResponse)
def get_history(db: Session = Depends(get_db)) -> HistoryResponse:
    entries = list_history_entries(db)
    return HistoryResponse(entries=entries)


@router.post("/history", response_model=HistoryResponse)
def add_history(payload: HistoryCreateRequest, db: Session = Depends(get_db)) -> HistoryResponse:
    create_history_entry(db=db, payload=payload)
    entries = list_history_entries(db)
    return HistoryResponse(entries=entries)


@router.get("/model-info", response_model=ModelInfoResponse)
def model_info() -> ModelInfoResponse:
    return get_model_info()


@router.post("/feedback", response_model=FeedbackResponse)
def feedback(payload: FeedbackRequest) -> FeedbackResponse:
    return FeedbackResponse(received=True, message="Feedback received for future model improvement.")

