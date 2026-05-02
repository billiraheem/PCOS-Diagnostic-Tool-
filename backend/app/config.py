from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List, Union
import json


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "PCOS Diagnostic Tool API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql://bills:najeebah@localhost:5432/pcos_db"
    
    # JWT Authentication
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS — accepts a JSON array string or a plain comma-separated string
    CORS_ORIGINS: Union[List[str], str] = ["http://localhost:3000"]

    def get_cors_origins(self) -> List[str]:
        if isinstance(self.CORS_ORIGINS, list):
            return self.CORS_ORIGINS
        # Try JSON parse first, then fall back to comma-split
        try:
            return json.loads(self.CORS_ORIGINS)
        except (json.JSONDecodeError, ValueError):
            return [o.strip() for o in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()