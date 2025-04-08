"""
Configuration settings for the application.

This module manages environment-specific configuration using Pydantic's
BaseSettings for validation and environment variable loading.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
import secrets


class Settings(BaseSettings):
    """Application configuration settings with environment variable support."""

    # Database settings
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"

    # Application mode
    TESTING: bool = False
    DEBUG: bool = False

    # API Security
    API_KEY: str = secrets.token_urlsafe(32)
    API_KEY_NAME: str = "X-API-Key"

    # CORS settings
    ALLOW_ORIGINS: list[str] = ["*"]
    ALLOW_CREDENTIALS: bool = True
    ALLOW_METHODS: list[str] = ["*"]
    ALLOW_HEADERS: list[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()


# Export settings instance for convenience
settings = get_settings()
