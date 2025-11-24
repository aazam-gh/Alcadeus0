from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.health import HealthResponse, ReadinessResponse
from app.core.config import get_settings
from app.database.engine import get_db

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check(settings: object = Depends(get_settings)) -> HealthResponse:
    """Health check endpoint."""
    settings = get_settings()
    return HealthResponse(
        status="healthy",
        app_name=settings.app_name,
        version="0.1.0"
    )


@router.get("/readiness", response_model=ReadinessResponse)
async def readiness_check(
    db: Session = Depends(get_db),
    settings: object = Depends(get_settings)
) -> ReadinessResponse:
    """Readiness check endpoint - validates database connectivity."""
    settings = get_settings()
    
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    
    return ReadinessResponse(
        status="ready" if db_status == "connected" else "not_ready",
        database=db_status,
        app_name=settings.app_name
    )
