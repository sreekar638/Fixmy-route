import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "FixRoute"
    APP_TAGLINE: str = "Tell us your problem. We'll tell you who can fix it."
    FOUNDER_NAME: str = "Sreekar"
    PRIMARY_MARKET: str = "India"
    APP_ENV: str = "development"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    SECRET_KEY: str = "fixroute-super-secure-secret-key-for-development-2026-min32bytes"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    DATABASE_URL: str = "sqlite:///./fixroute.db"
    CORS_ORIGINS: str = "http://localhost:8000,http://127.0.0.1:8000,http://localhost:3000"
    
    AI_PROVIDER: str = "none"  # "none", "gemini", or "openai"
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    
    ADMIN_EMAIL: str = "admin@fixroute.in"
    ADMIN_PASSWORD: str = "AdminSecureFixRoute2026!"

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }

    @property
    def cors_origin_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

settings = Settings()
