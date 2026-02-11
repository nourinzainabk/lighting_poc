from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Required environment variables
    ROBOFLOW_API_KEY: str
    SECRET_KEY: str
    DATABASE_URL: str

    CORS_ORIGINS: List[str]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
