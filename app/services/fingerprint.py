import hashlib
import json

from app.schemas.incident import AlertIn


def generate_alert_fingerprint(alert: AlertIn) -> str:
    """Create a stable fingerprint so repeated alerts do not create duplicate incidents."""
    fingerprint_payload = {
        "title": alert.title.strip().lower(),
        "service": alert.service.strip().lower(),
        "severity": alert.severity,
        "source": alert.source.strip().lower(),
        "environment": alert.environment.strip().lower(),
        "description": (alert.description or "").strip().lower(),
        "metadata": alert.metadata,
    }

    normalized_payload = json.dumps(
        fingerprint_payload,
        sort_keys=True,
        separators=(",", ":"),
    )

    return hashlib.sha256(normalized_payload.encode("utf-8")).hexdigest()
