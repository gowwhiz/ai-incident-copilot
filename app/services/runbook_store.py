Runbook = dict[str, list[str] | str]


DEFAULT_RUNBOOK: Runbook = {
    "first_checks": [
        "Check recent deployments for the affected service.",
        "Inspect application logs for new errors or timeouts.",
        "Compare current error rate and latency against the previous baseline.",
    ],
    "rollback_plan": (
        "If a recent deployment correlates with the incident, roll back to the last known "
        "good version."
    ),
    "escalation_path": (
        "Escalate to the owning service team if customer impact continues for more than "
        "15 minutes."
    ),
}


RUNBOOKS: dict[str, Runbook] = {
    "checkout-api": {
        "first_checks": [
            "Check payment gateway timeout and error metrics.",
            "Inspect checkout-api dependency latency by endpoint.",
            "Review database connection pool saturation.",
            "Verify payment provider status page and internal dependency dashboards.",
        ],
        "rollback_plan": (
            "Roll back checkout-api if a recent release changed payment client timeout, "
            "retry, or gateway behavior."
        ),
        "escalation_path": (
            "Escalate to payments-platform on-call and notify customer-support leadership "
            "for customer-facing checkout failures."
        ),
    },
    "auth-service": {
        "first_checks": [
            "Check identity provider availability.",
            "Inspect token signing key rotation events.",
            "Verify JWKS cache refresh behavior.",
            "Review token validation error rate by client application.",
            "Confirm whether login failures are isolated to one environment or all traffic.",
        ],
        "rollback_plan": (
            "Roll back auth-service if a recent deploy changed token validation, cache "
            "refresh, or identity provider integration."
        ),
        "escalation_path": (
            "Escalate to identity-platform on-call for sustained login or token validation "
            "failures."
        ),
    },
}


def get_runbook_for_service(service: str) -> Runbook:
    return RUNBOOKS.get(service, DEFAULT_RUNBOOK)
