from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = "AI Incident Copilot"
    app_env: str = "local"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()

app = FastAPI(
    title=settings.app_name,
    description="AI-assisted incident response backend for production support workflows.",
    version="0.1.0",
)


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    """Return basic service health information."""

    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.app_env,
    }
