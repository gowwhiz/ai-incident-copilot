from datetime import UTC, datetime, timedelta


def search_related_logs(
    service: str,
    environment: str,
    metadata: dict,
) -> list[dict[str, str]]:
    """Return related logs for an alert.

    This commit uses deterministic mock data so the project runs locally without Datadog,
    Splunk, CloudWatch, or OpenSearch credentials. The function boundary is intentionally
    shaped like a real adapter so it can later be swapped for a production log provider.
    """
    region = metadata.get("region", "us-east-1")
    now = datetime.now(UTC)

    if service == "checkout-api":
        return [
            {
                "timestamp": (now - timedelta(minutes=5)).isoformat(),
                "service": service,
                "environment": environment,
                "region": region,
                "level": "ERROR",
                "message": "payment_provider_timeout after 3000ms while authorizing order",
            },
            {
                "timestamp": (now - timedelta(minutes=4)).isoformat(),
                "service": service,
                "environment": environment,
                "region": region,
                "level": "WARN",
                "message": "retry budget exhausted for downstream payment-service",
            },
            {
                "timestamp": (now - timedelta(minutes=3)).isoformat(),
                "service": service,
                "environment": environment,
                "region": region,
                "level": "ERROR",
                "message": "HTTP 502 returned from payment-service upstream gateway",
            },
        ]

    if service == "auth-service":
        return [
            {
                "timestamp": (now - timedelta(minutes=6)).isoformat(),
                "service": service,
                "environment": environment,
                "region": region,
                "level": "ERROR",
                "message": "token_validation_failed due to jwks_cache_miss",
            },
            {
                "timestamp": (now - timedelta(minutes=5)).isoformat(),
                "service": service,
                "environment": environment,
                "region": region,
                "level": "WARN",
                "message": "increased latency fetching identity provider signing keys",
            },
        ]

    return [
        {
            "timestamp": (now - timedelta(minutes=5)).isoformat(),
            "service": service,
            "environment": environment,
            "region": region,
            "level": "WARN",
            "message": "elevated latency detected with limited correlated log context",
        }
    ]
