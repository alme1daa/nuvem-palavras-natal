import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Nuvem de Palavras de Natal SENAI"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./local_natal.db")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "natal_senai_secret_key_change_me_in_prod")
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "senai2026")
    PUBLIC_URL: str = os.getenv("PUBLIC_URL", "http://localhost:8000")
    MAX_SUBMISSIONS_PER_IP_MINUTE: int = 5

    class Config:
        env_file = ".env"

settings = Settings()