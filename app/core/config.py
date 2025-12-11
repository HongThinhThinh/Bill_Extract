from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Bill Extractor"
    API_V1_STR: str = "/api/v1"
    OPENROUTER_API_KEY: str
    OPENROUTER_MODEL: str = "google/gemini-2.0-flash-001"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
