from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class ScanHistory(Base):
    __tablename__ = "scan_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    state: Mapped[str] = mapped_column(String(32), nullable=False)
    sleep_hours: Mapped[float] = mapped_column(Float, nullable=False)
    screen_time: Mapped[float] = mapped_column(Float, nullable=False)
    exercise_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    stress_level: Mapped[int] = mapped_column(Integer, nullable=False)
    model_version: Mapped[str] = mapped_column(String(32), nullable=False)

