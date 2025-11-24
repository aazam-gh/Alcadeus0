from pydantic import BaseModel
from typing import Optional


class HealthResponse(BaseModel):
    """Health check response schema."""
    status: str
    app_name: str
    version: str = "0.1.0"


class ReadinessResponse(BaseModel):
    """Readiness check response schema."""
    status: str
    database: str
    app_name: str
