from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.incident import Incident
from app.schemas.incident import AlertIn, IncidentOut, ResolveIncidentIn
from app.services.fingerprint import generate_alert_fingerprint

router = APIRouter(prefix="/incidents", tags=["incidents"])

DbSession = Annotated[Session, Depends(get_db)]


@router.post("/ingest", response_model=IncidentOut, status_code=status.HTTP_201_CREATED)
def ingest_alert(alert: AlertIn, db: DbSession) -> Incident:
    """Create a new incident from an incoming alert or return the existing duplicate."""

    alert_fingerprint = generate_alert_fingerprint(alert)

    existing_incident = db.scalar(
        select(Incident).where(Incident.alert_fingerprint == alert_fingerprint)
    )
    if existing_incident:
        return existing_incident

    incident = Incident(
        title=alert.title,
        service=alert.service,
        severity=alert.severity,
        status="open",
        source=alert.source,
        environment=alert.environment,
        alert_fingerprint=alert_fingerprint,
        description=alert.description,
        raw_payload=alert.metadata,
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    return incident


@router.get("", response_model=list[IncidentOut])
def list_incidents(
    db: DbSession,
    service: Annotated[str | None, Query(max_length=120)] = None,
    severity: Annotated[str | None, Query(max_length=40)] = None,
    status_filter: Annotated[str | None, Query(alias="status", max_length=40)] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 25,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[Incident]:
    """List incidents with optional filters for service, severity, and status."""

    query: Select[tuple[Incident]] = select(Incident)

    if service:
        query = query.where(Incident.service == service)
    if severity:
        query = query.where(Incident.severity == severity)
    if status_filter:
        query = query.where(Incident.status == status_filter)

    query = query.order_by(Incident.created_at.desc()).limit(limit).offset(offset)

    return list(db.scalars(query).all())


@router.get("/{incident_id}", response_model=IncidentOut)
def get_incident(incident_id: int, db: DbSession) -> Incident:
    """Return one incident by ID."""

    incident = db.get(Incident, incident_id)
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found",
        )

    return incident


@router.post("/{incident_id}/resolve", response_model=IncidentOut)
def resolve_incident(
    incident_id: int,
    payload: ResolveIncidentIn,
    db: DbSession,
) -> Incident:
    """Mark an incident as resolved and store the resolution notes."""

    incident = db.get(Incident, incident_id)
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found",
        )

    incident.status = "resolved"
    incident.resolution_summary = payload.resolution_summary

    db.add(incident)
    db.commit()
    db.refresh(incident)

    return incident
