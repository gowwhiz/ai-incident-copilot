from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from app.core.config import get_settings
from app.db.session import Base, engine
from app.models.incident import Incident  # noqa: F401 - imported so SQLAlchemy registers the model


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Initialize application resources when the API starts."""

    Base.metadata.create_all(bind=engine)
    yield


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="AI-assisted incident response backend for production support workflows.",
    version="0.2.0",
    lifespan=lifespan,
)


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    """Return basic service health information."""

    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.app_env,
        "database": "configured",
    }
