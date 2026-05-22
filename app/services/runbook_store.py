DEFAULT_RUNBOOK = {
    "owner_team": "platform-support",
    "first_checks": [
        "Confirm whether the alert is isolated to one region or global.",
        "Review recent deployments for the affected service.",
        "Check upstream and downstream dependency health.",
        "Compare current error rate and latency against the previous baseline.",
    ],
    "rollback_plan": "If a recent deployment correlates with the incident, roll back to the last known good version.",
    "escalation_path": "Escalate to the owning service team if customer impact continues for more than 15 minutes.",
}


RUNBOOKS = {
    "checkout-api": {
        "owner_team": "payments-platform",
        "first_checks": [
            "Check payment-service latency and timeout rate.",
            "Review checkout-api deployment history for the last 60 minutes.",
            "Inspect gateway 5xx responses by region.",
            "Verify payment provider status page and internal dependency dashboards.",
        ],
        "rollback_plan": "Roll back checkout-api if a recent release changed payment client timeout, retry, or gateway behavior.",
        "escalation_path": "Escalate to payments-platform on-call and notify customer-support leadership for customer-facing checkout failures.",
    },
    "auth-service": {
        "owner_team": "identity-platform",
        "first_checks": [
            "Check identity provider availability.",
            "Verify JWKS cache refresh behavior.",
            "Review token validation error rate by client application.",
            "Confirm whether login failures are isolated to one environment or all production traffic.",
        ],
        "rollback_plan": "Roll back auth-service if a recent deploy changed token validation, cache refresh, or identity provider integration.",
        "escalation_path": "Escalate to identity-platform on-call for sustained login or token validation failures.",
    },
}


def get_runbook_for_service(service: str) -> dict:
    """Fetch service-specific runbook guidance, falling back to a default runbook."""
    return RUNBOOKS.get(service, DEFAULT_RUNBOOK)
