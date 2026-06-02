from dataclasses import dataclass
from uuid import uuid4

from app.models.incident import Incident


@dataclass(frozen=True)
class IntegrationResult:
    action_type: str
    destination: str
    external_reference: str
    summary: str


def build_incident_brief(incident: Incident) -> str:
    recommended_actions = incident.recommended_actions or []
    actions_text = "; ".join(recommended_actions[:3]) or "Review logs and runbook context."

    return (
        f"[{incident.severity.upper()}] {incident.title} affecting {incident.service}. "
        f"Probable cause: {incident.probable_cause or 'unknown'}. "
        f"Recommended next steps: {actions_text}"
    )


class MockSlackNotifier:
    def send_incident_alert(
        self,
        incident: Incident,
        channel: str,
        note: str | None = None,
    ) -> IntegrationResult:
        brief = build_incident_brief(incident)
        note_text = f" Operator note: {note}" if note else ""
        message_id = f"mock-slack-{uuid4().hex[:10]}"

        return IntegrationResult(
            action_type="slack_notification",
            destination=channel,
            external_reference=message_id,
            summary=f"Sent incident brief to {channel}: {brief}{note_text}",
        )


class MockJiraClient:
    def create_incident_ticket(self, incident: Incident, project_key: str) -> IntegrationResult:
        ticket_key = f"{project_key}-{incident.id:04d}"
        brief = build_incident_brief(incident)

        return IntegrationResult(
            action_type="jira_ticket",
            destination=project_key,
            external_reference=ticket_key,
            summary=f"Created Jira incident ticket {ticket_key}: {brief}",
        )
