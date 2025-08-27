# app/core/config.py
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    APP_NAME: str = "Zenomy Dataset Manager"
    DATABASE_URL: str = f"sqlite:///{Path(__file__).parent.parent.parent / 'data' / 'database.db'}"
    DEBUG: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
