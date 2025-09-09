"""Configuration management for the SQL Agent."""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings."""
    
    # Gradient AI Configuration
    gradient_access_token: str = Field(..., env="GRADIENT_ACCESS_TOKEN")
    gradient_workspace_id: str = Field(..., env="GRADIENT_WORKSPACE_ID")
    
    # Database Configuration
    database_url: Optional[str] = Field(None, env="DATABASE_URL")
    
    # Safety Configuration
    allow_production_connections: bool = Field(False, env="ALLOW_PRODUCTION_CONNECTIONS")
    max_generated_records: int = Field(1000, env="MAX_GENERATED_RECORDS")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
