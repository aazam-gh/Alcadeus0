from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database configuration
    database_url: str
    database_echo: bool = False
    
    # FSM API configuration
    fsm_api_key: str
    fsm_api_url: str = "https://api.fieldsolutionsmanager.com"
    
    # Optional LLM configuration
    llm_api_key: str | None = None
    
    # Application settings
    app_name: str = "Field Solutions Backend"
    debug: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
