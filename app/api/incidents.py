from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.incident import Incident
from app.schemas.incident import AlertIn, IncidentOut, ResolveIncidentIn
from app.services.ai_analyzer import analyze_incident
from app.services.fingerprint import generate_alert_fingerprint
from app.services.log_search import search_related_logs
from app.services.runbook_store import get_runbook_for_service

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.post("/ingest", response_model=IncidentOut, status_code=201)
def ingest_alert(alert: AlertIn, db: Session = Depends(get_db)) -> Incident:
    fingerprint = generate_alert_fingerprint(alert)

    existing_incident = db.scalar(
        select(Incident).where(Incident.alert_fingerprint == fingerprint)
    )

    if existing_incident is not None:
        return existing_incident

    related_logs = search_related_logs(
        service=alert.service,
        environment=alert.environment,
        metadata=alert.metadata,
    )
    runbook = get_runbook_for_service(alert.service)
    analysis = analyze_incident(alert=alert, logs=related_logs, runbook=runbook)

    incident = Incident(
        title=alert.title,
        service=alert.service,
        severity=alert.severity,
        source=alert.source,
        environment=alert.environment,
        description=alert.description,
        raw_payload=alert.metadata,
        alert_fingerprint=fingerprint,
        symptoms=analysis.symptoms,
        probable_cause=analysis.probable_cause,
        recommended_actions=analysis.recommended_actions,
        postmortem_summary=analysis.postmortem_summary,
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    return incident


@router.get("", response_model=list[IncidentOut])
def list_incidents(
    db: Session = Depends(get_db),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[Incident]:
    statement = (
        select(Incident)
        .order_by(Incident.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    return list(db.scalars(statement).all())


@router.get("/{incident_id}", response_model=IncidentOut)
def get_incident(incident_id: int, db: Session = Depends(get_db)) -> Incident:
    incident = db.get(Incident, incident_id)

    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")

    return incident


@router.post("/{incident_id}/resolve", response_model=IncidentOut)
def resolve_incident(
    incident_id: int,
    payload: ResolveIncidentIn,
    db: Session = Depends(get_db),
) -> Incident:
    incident = db.get(Incident, incident_id)

    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")

    incident.status = "resolved"
    incident.resolution_summary = payload.resolution_summary

    db.add(incident)
    db.commit()
    db.refresh(incident)

    return incident
