from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.api import health, accounts

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Backend service for field solutions management",
    version="0.1.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(accounts.router, prefix="/api")


@app.get("/")
def read_root():
    """Root endpoint."""
    return {
        "app_name": settings.app_name,
        "version": "0.1.0",
        "docs_url": "/api/docs",
        "openapi_url": "/api/openapi.json"
    }
