from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_hostname: str
    postgres_port: str
    postgres_db: str
    openai_api_key: str

    class Config:
        env_file = str(Path(__file__).resolve().parent.parent / ".env")


settings = Settings()
