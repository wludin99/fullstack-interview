"""Configuration settings for the Tender Checklist App."""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Anthropic API
    anthropic_api_key: str = "test-key"  # Will be overridden by environment variable
    anthropic_model: str = "claude-3-5-sonnet-20241022"
    
    # Database
    database_url: str = "sqlite:///./tender_checklist.db"
    
    # Application
    debug: bool = True
    log_level: str = "INFO"
    
    # File upload
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: list[str] = ["application/pdf"]
    
    class Config:
        env_file = ".env"


# Global settings instance
settings = Settings()
