"""
Application configuration settings
"""

from typing import List, Union
from pydantic import validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "BreastCare Pro"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS settings
    # Les origines sont définies via la variable d'environnement BACKEND_CORS_ORIGINS
    # Format: URL1,URL2,URL3 (séparées par des virgules)
    # Valeurs par défaut pour le développement local
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        raise ValueError(v)

    # Database settings
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "breastcare"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "breastcare_db"
    
    @property
    def DATABASE_URL(self) -> str:
        # Check if DATABASE_URL is set in environment (for production deployments)
        # This allows Render, Railway, etc. to inject their database URL
        import os
        env_db_url = os.getenv("DATABASE_URL")
        if env_db_url:
            return env_db_url
        
        # For local development, use SQLite
        return f"sqlite:///./breastcare.db"

    # Security settings
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # ML Model settings
    MODEL_PATH: str = "models/breastcare_model.h5"
    MODEL_CONFIDENCE_THRESHOLD: float = 0.7
    
    # File upload settings
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS: List[str] = [".png", ".jpg", ".jpeg", ".dcm"]
    
    # External services
    REDIS_URL: str = "redis://localhost:6379"
    
    # Email settings (for notifications)
    SMTP_TLS: bool = True
    SMTP_PORT: int = 587
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAILS_FROM_EMAIL: str = "noreply@breastcare.com"
    EMAILS_FROM_NAME: str = "BreastCare Pro"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
