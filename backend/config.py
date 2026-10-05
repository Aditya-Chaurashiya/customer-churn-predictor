import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/customer_churn_db"
    MODEL_DIR: str = "models/"
    DATA_DIR: str = "data/"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    MODEL_VERSION: str = "1.0.0"

    class Config:
        env_file = ".env"

settings = Settings()
