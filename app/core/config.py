from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "Nukev AI Backend API"
    API_V1_STR: str = "/api/v1"
    
    # CORS setup
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] | List[str] = []
    
    # LLM Configuration
    GROQ_API_KEY: str
    
    # TMDB Configuration
    TMDB_API_KEY: str
    TMDB_READ_ACCESS_TOKEN: str

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        case_sensitive=True
    )

settings = Settings()
