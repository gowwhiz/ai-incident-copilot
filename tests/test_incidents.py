from fastapi.testclient import TestClient

from app.db.session import Base, engine
from app.main import app

client = TestClient(app)


def reset_database() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_health_check_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["copilot"] == "enabled"


def test_ingest_alert_creates_ai_enriched_incident() -> None:
    reset_database()

    payload = {
        "title": "Checkout API latency spike",
        "service": "checkout-api",
        "severity": "high",
        "source": "datadog",
        "environment": "production",
        "description": "P95 latency exceeded threshold for 10 minutes",
        "metadata": {"region": "us-east-1", "team": "payments"},
    }

    response = client.post("/incidents/ingest", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["service"] == "checkout-api"
    assert data["status"] == "open"
    assert data["alert_fingerprint"] is not None
    assert "Elevated" in data["symptoms"]
    assert data["probable_cause"] is not None
    assert len(data["recommended_actions"]) >= 3
    assert data["postmortem_summary"] is not None


def test_ingest_alert_deduplicates_repeated_alerts() -> None:
    reset_database()

    payload = {
        "title": "Checkout API latency spike",
        "service": "checkout-api",
        "severity": "high",
        "source": "datadog",
        "environment": "production",
        "description": "P95 latency exceeded threshold for 10 minutes",
        "metadata": {"region": "us-east-1", "team": "payments"},
    }

    first_response = client.post("/incidents/ingest", json=payload)
    second_response = client.post("/incidents/ingest", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 201
    assert first_response.json()["id"] == second_response.json()["id"]
    assert first_response.json()["alert_fingerprint"] == second_response.json()["alert_fingerprint"]

    list_response = client.get("/incidents")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1


def test_resolve_incident_updates_status_and_summary() -> None:
    reset_database()

    ingest_response = client.post(
        "/incidents/ingest",
        json={
            "title": "Auth service elevated 5xx errors",
            "service": "auth-service",
            "severity": "critical",
            "source": "splunk",
            "environment": "production",
            "description": "Authentication requests are failing intermittently",
            "metadata": {"region": "us-east-1"},
        },
    )
    incident_id = ingest_response.json()["id"]

    resolve_response = client.post(
        f"/incidents/{incident_id}/resolve",
        json={
            "resolution_summary": "Rotated the failing signing key and confirmed login errors returned to baseline."
        },
    )

    assert resolve_response.status_code == 200
    data = resolve_response.json()
    assert data["status"] == "resolved"
    assert "signing key" in data["resolution_summary"]
