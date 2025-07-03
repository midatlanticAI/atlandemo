"""
Settings configuration module for AtlanDemo.

This module provides environment-based configuration management using Pydantic Settings.
Demonstrates secure configuration practices and environment variable handling.
"""

import os
from functools import lru_cache
from typing import Optional, List

from pydantic import BaseSettings, Field, validator
from pydantic_settings import BaseSettings as PydanticBaseSettings


class Settings(PydanticBaseSettings):
    """
    Application settings with environment variable support.
    
    This class demonstrates secure configuration management including:
    - Environment variable binding
    - Default values
    - Validation
    - Type safety
    """
    
    # Application settings
    app_name: str = Field(default="AtlanDemo", env="APP_NAME")
    debug: bool = Field(default=False, env="DEBUG")
    environment: str = Field(default="development", env="ENVIRONMENT")
    
    # Server settings
    host: str = Field(default="127.0.0.1", env="HOST")
    port: int = Field(default=8000, env="PORT")
    
    # Security settings
    secret_key: str = Field(default="your-secret-key-change-in-production", env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Database settings
    database_url: str = Field(default="sqlite:///./atlandemo.db", env="DATABASE_URL")
    database_echo: bool = Field(default=False, env="DATABASE_ECHO")
    
    # Redis settings (if using Redis)
    redis_url: Optional[str] = Field(default=None, env="REDIS_URL")
    
    # CORS settings
    cors_origins: List[str] = Field(default=["*"], env="CORS_ORIGINS")
    
    # Logging settings
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(
        default="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        env="LOG_FORMAT"
    )
    
    # External API settings
    api_timeout: int = Field(default=30, env="API_TIMEOUT")
    max_retries: int = Field(default=3, env="MAX_RETRIES")
    
    # Security headers
    security_headers: bool = Field(default=True, env="SECURITY_HEADERS")
    
    @validator("environment")
    def validate_environment(cls, v):
        """Validate environment setting."""
        valid_envs = ["development", "staging", "production"]
        if v not in valid_envs:
            raise ValueError(f"Environment must be one of: {valid_envs}")
        return v
    
    @validator("log_level")
    def validate_log_level(cls, v):
        """Validate log level setting."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of: {valid_levels}")
        return v.upper()
    
    @validator("cors_origins", pre=True)
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @validator("secret_key")
    def validate_secret_key(cls, v, values):
        """Validate secret key in production."""
        if values.get("environment") == "production":
            if v == "your-secret-key-change-in-production":
                raise ValueError("Must set SECRET_KEY in production environment")
            if len(v) < 32:
                raise ValueError("Secret key must be at least 32 characters long")
        return v
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment == "development"
    
    @property
    def is_debug(self) -> bool:
        """Check if debug mode is enabled."""
        return self.debug or self.is_development
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings with caching.
    
    Uses LRU cache to ensure settings are loaded only once.
    This is a common pattern for configuration management.
    
    Returns:
        Settings: Application settings instance
    """
    return Settings() 