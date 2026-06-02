from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Severity = Literal["low", "medium", "high", "critical"]
IncidentStatus = Literal["open", "investigating", "resolved"]


class AlertIn(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    service: str = Field(..., min_length=2, max_length=120)
    severity: Severity = "medium"
    source: str = Field(default="manual", max_length=80)
    environment: str = Field(default="production", max_length=80)
    description: str | None = None
    metadata: dict = Field(default_factory=dict)


class IncidentActionOut(BaseModel):
    id: int
    incident_id: int
    action_type: str
    status: str
    destination: str
    external_reference: str | None
    summary: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class IncidentOut(BaseModel):
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

    model_config = ConfigDict(from_attributes=True)


class ResolveIncidentIn(BaseModel):
    resolution_summary: str = Field(..., min_length=5)


class EscalateIncidentIn(BaseModel):
    slack_channel: str = Field(default="#incident-response", min_length=2, max_length=80)
    jira_project_key: str = Field(default="INC", min_length=2, max_length=10)
    note: str | None = Field(default=None, max_length=500)


class EscalationOut(BaseModel):
    incident: IncidentOut
    actions: list[IncidentActionOut]
