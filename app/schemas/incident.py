from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Severity = Literal["low", "medium", "high", "critical"]
IncidentStatus = Literal["open", "investigating", "resolved"]


class AlertIn(BaseModel):
    """Incoming alert payload received by the incident copilot."""

    title: str = Field(..., min_length=3, max_length=255)
    service: str = Field(..., min_length=2, max_length=120)
    severity: Severity = "medium"
    source: str = Field(default="manual", max_length=80)
    environment: str = Field(default="production", max_length=80)
    description: str | None = None
    metadata: dict = Field(default_factory=dict)


class IncidentOut(BaseModel):
    """API response model for incidents stored in the system."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    service: str
    severity: str
    status: str
    source: str
    environment: str
    alert_fingerprint: str | None
    description: str | None
    symptoms: str | None
    probable_cause: str | None
    recommended_actions: list[str] | None
    postmortem_summary: str | None
    resolution_summary: str | None
    created_at: datetime
    updated_at: datetime


class ResolveIncidentIn(BaseModel):
    """Payload used later when marking an incident as resolved."""

    resolution_summary: str = Field(..., min_length=5)
