from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router
from app.database.session import initialize_database


app = FastAPI(
    title="NeuroPulse API",
    version="0.1.0",
    description="Educational lifestyle-state prediction API for NeuroPulse.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.on_event("startup")
def on_startup() -> None:
    initialize_database()

