from pydantic import BaseModel

from app.schemas.incident import AlertIn


class IncidentAnalysis(BaseModel):
    symptoms: str
    probable_cause: str
    recommended_actions: list[str]
    postmortem_summary: str


def analyze_incident(
    alert: AlertIn,
    logs: list[dict[str, str]],
    runbook: dict,
) -> IncidentAnalysis:
    """Generate investigation guidance from an alert, related logs, and runbook context.

    This is a deterministic mock analyzer for local development. It is intentionally
    designed behind a service boundary so it can later be replaced with an OpenAI,
    Anthropic, or internal LLM provider without changing the API layer.
    """
    joined_logs = " ".join(log["message"].lower() for log in logs)

    if "payment_provider_timeout" in joined_logs or "payment-service" in joined_logs:
        probable_cause = (
            "The checkout-api appears to be failing because calls to payment-service or "
            "the external payment provider are timing out and returning upstream errors."
        )
        symptoms = (
            "Elevated checkout failures, exhausted retry attempts, and HTTP 502 responses "
            "were found in logs for the affected production service."
        )
    elif "jwks_cache_miss" in joined_logs or "token_validation_failed" in joined_logs:
        probable_cause = (
            "The auth-service appears to be failing token validation because signing key "
            "metadata is unavailable or not refreshing correctly."
        )
        symptoms = (
            "Token validation errors and identity provider key-fetch latency were found "
            "in the related logs."
        )
    else:
        probable_cause = (
            "The incident appears related to elevated latency or errors in the affected "
            "service, but the mock log context is not specific enough to identify one root cause."
        )
        symptoms = (
            "The service is reporting abnormal behavior and related logs show elevated "
            "latency or warning-level events."
        )

    recommended_actions = [
        *runbook.get("first_checks", []),
        runbook.get("rollback_plan", "Review rollback options for the affected service."),
        runbook.get("escalation_path", "Escalate to the owning service team if impact continues."),
    ]

    postmortem_summary = (
        f"{alert.service} triggered a {alert.severity} incident in {alert.environment}. "
        f"Initial analysis indicates: {probable_cause}"
    )

    return IncidentAnalysis(
        symptoms=symptoms,
        probable_cause=probable_cause,
        recommended_actions=recommended_actions,
        postmortem_summary=postmortem_summary,
    )
