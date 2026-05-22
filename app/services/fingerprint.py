import hashlib
import json
from typing import Any

from app.schemas.incident import AlertIn


def _normalize(value: Any) -> Any:
    """Normalize values so semantically identical alerts produce the same hash."""

    if isinstance(value, str):
        return " ".join(value.lower().strip().split())

    if isinstance(value, dict):
        return {str(key): _normalize(value[key]) for key in sorted(value)}

    if isinstance(value, list):
        return [_normalize(item) for item in value]

    return value


def generate_alert_fingerprint(alert: AlertIn) -> str:
    """Create a deterministic fingerprint used to deduplicate repeated alerts."""

    fingerprint_source = {
        "title": alert.title,
        "service": alert.service,
        "severity": alert.severity,
        "source": alert.source,
        "environment": alert.environment,
        "metadata": alert.metadata,
    }

    normalized_payload = _normalize(fingerprint_source)
    encoded_payload = json.dumps(normalized_payload, sort_keys=True, separators=(",", ":"))

    return hashlib.sha256(encoded_payload.encode("utf-8")).hexdigest()
