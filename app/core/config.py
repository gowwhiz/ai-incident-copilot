from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Incident Copilot"
    app_env: str = "local"
    log_level: str = "INFO"
    database_url: str = "sqlite:///./incident_copilot.db"
    llm_provider: str = "mock"
    openai_api_key: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
