from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.scan_history import ScanHistory
from app.schemas.requests import HistoryCreateRequest
from app.schemas.responses import HistoryEntryResponse


def create_history_entry(db: Session, payload: HistoryCreateRequest) -> HistoryEntryResponse:
    entry = ScanHistory(
        score=payload.score,
        state=payload.state,
        sleep_hours=payload.sleep_hours,
        screen_time=payload.screen_time,
        exercise_minutes=payload.exercise_minutes,
        stress_level=payload.stress_level,
        model_version=payload.model_version,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return HistoryEntryResponse(
        id=entry.id,
        created_at=entry.created_at.isoformat(),
        score=entry.score,
        state=entry.state,
        sleep_hours=entry.sleep_hours,
        screen_time=entry.screen_time,
        exercise_minutes=entry.exercise_minutes,
        stress_level=entry.stress_level,
        model_version=entry.model_version,
    )


def list_history_entries(db: Session) -> list[HistoryEntryResponse]:
    entries = db.query(ScanHistory).order_by(ScanHistory.created_at.desc()).all()
    return [
        HistoryEntryResponse(
            id=entry.id,
            created_at=entry.created_at.isoformat(),
            score=entry.score,
            state=entry.state,
            sleep_hours=entry.sleep_hours,
            screen_time=entry.screen_time,
            exercise_minutes=entry.exercise_minutes,
            stress_level=entry.stress_level,
            model_version=entry.model_version,
        )
        for entry in entries
    ]

