from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = "AI Incident Copilot"
    app_env: str = "local"
    log_level: str = "INFO"
    database_url: str = "sqlite:///./incident_copilot.db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings.

    Caching prevents the settings object from being rebuilt on every import while
    still keeping configuration centralized and easy to override in tests later.
    """

    return Settings()
