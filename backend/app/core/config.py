from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
import os

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Image Classification Service"
    VERSION: str = "1.0.0"
    
    # CORS Settings
    ALLOWED_HOSTS: List[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"]
    )
    
    # File Upload Settings
    MAX_FILE_SIZE: int = Field(default=10 * 1024 * 1024)  # 10MB
    ALLOWED_IMAGE_EXTENSIONS: List[str] = Field(
        default=[".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]
    )
    UPLOAD_DIR: str = Field(default="uploads")
    
    # Database Settings
    DATABASE_URL: str = Field(
        default="postgresql://user:password@localhost:5432/image_classification_db",
        env="DATABASE_URL"
    )
    
    # AI/ML Settings
    GOOGLE_CLOUD_PROJECT: str = Field(default="", env="GOOGLE_CLOUD_PROJECT")
    GOOGLE_CLOUD_CREDENTIALS: str = Field(default="", env="GOOGLE_CLOUD_CREDENTIALS")
    
    # Model Settings
    DEFAULT_MODEL: str = Field(default="mock")
    CONFIDENCE_THRESHOLD: float = Field(default=0.1)
    
    # Security Settings
    SECRET_KEY: str = Field(
        default="your-secret-key-change-this-in-production",
        env="SECRET_KEY"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    
    # Environment
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=True, env="DEBUG")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()