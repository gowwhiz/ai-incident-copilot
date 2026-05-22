from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.incidents import router as incidents_router
from app.core.config import get_settings
from app.db.session import Base, engine
from app.models.incident import Incident  # noqa: F401 - imported so SQLAlchemy registers the model


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(bind=engine)
    yield


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.4.0",
    description="AI-assisted incident triage and root-cause analysis service.",
    lifespan=lifespan,
)

app.include_router(incidents_router)


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.app_env,
        "database": "configured",
        "copilot": "enabled",
    }
