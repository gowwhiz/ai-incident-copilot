# AI Incident Copilot

AI Incident Copilot is a Python/FastAPI backend that simulates how a production-support, SRE, or platform engineering team could triage incidents faster with alert deduplication, log context, runbook context, AI-generated investigation guidance, and escalation workflows.

## Current stage

**Commit update: Incident escalation workflow with collaboration actions**

This stage adds a realistic incident escalation layer on top of the existing AI-enriched incident workflow.

New capabilities:

- Escalate an incident to mock Slack and Jira integrations
- Move open incidents into `investigating` status during escalation
- Store outbound collaboration actions in an audit table
- Retrieve all actions taken for an incident
- Test the escalation workflow end-to-end

## Features

- FastAPI service with interactive Swagger docs
- SQLite persistence through SQLAlchemy
- Alert ingestion endpoint
- Alert fingerprinting and deduplication
- Incident list/detail endpoints
- Incident resolution endpoint
- Mock log-search enrichment
- Mock runbook retrieval
- Deterministic AI-style incident analysis
- Mock Slack incident notification
- Mock Jira incident ticket creation
- Incident action audit trail
- Automated API tests with `pytest`
- Ruff linting
- Docker and Docker Compose support
- GitHub Actions CI pipeline
- Architecture documentation with Mermaid diagrams

## Project structure

```text
ai-incident-copilot/
├── app/
│   ├── api/
│   │   └── incidents.py
│   ├── core/
│   │   └── config.py
│   ├── db/
│   │   └── session.py
│   ├── models/
│   │   ├── incident.py
│   │   └── incident_action.py
│   ├── schemas/
│   │   └── incident.py
│   ├── services/
│   │   ├── ai_analyzer.py
│   │   ├── collaboration.py
│   │   ├── fingerprint.py
│   │   ├── log_search.py
│   │   └── runbook_store.py
│   └── main.py
├── docs/
│   └── architecture.md
├── tests/
│   └── test_incidents.py
├── .github/workflows/
│   └── ci.yml
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Requirements

Use Python 3.12 for the smoothest install experience.

Python 3.14 may try to build some dependencies from source on Windows, which can cause install errors with packages like `pydantic-core`.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

On Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Open the API docs:

```text
http://127.0.0.1:8000/docs
```

## Run with Docker

```bash
cp .env.example .env
docker compose up --build
```

On Windows PowerShell:

```powershell
copy .env.example .env
docker compose up --build
```

Then open:

```text
http://127.0.0.1:8000/docs
```

## Run tests

```bash
pytest -q
```

Run linting:

```bash
ruff check app tests
```

## API endpoints

```text
GET  /health
POST /incidents/ingest
GET  /incidents
GET  /incidents/{incident_id}
POST /incidents/{incident_id}/resolve
POST /incidents/{incident_id}/escalate
GET  /incidents/{incident_id}/actions
```

## Example: ingest an alert

Use `POST /incidents/ingest` with this body:

```json
{
  "title": "Checkout API latency spike",
  "service": "checkout-api",
  "severity": "high",
  "source": "datadog",
  "environment": "production",
  "description": "P95 latency exceeded threshold for 10 minutes",
  "metadata": {
    "region": "us-east-1",
    "team": "payments"
  }
}
```

The response includes AI-style investigation fields:

```json
{
  "symptoms": "Elevated latency and downstream timeout errors detected for checkout-api.",
  "probable_cause": "The most likely cause is timeout failures from a downstream payment provider.",
  "recommended_actions": [
    "Check payment gateway timeout and error metrics.",
    "Inspect checkout-api dependency latency by endpoint.",
    "Review database connection pool saturation."
  ],
  "postmortem_summary": "checkout-api experienced elevated latency likely related to downstream payment-provider timeouts."
}
```

## Example: escalate an incident

After creating an incident, escalate it with:

```text
POST /incidents/{incident_id}/escalate
```

Example request body:

```json
{
  "slack_channel": "#sev-response",
  "jira_project_key": "INC",
  "note": "Escalating after sustained customer-impacting latency."
}
```

The service will:

1. Build a short incident brief from the AI-generated analysis.
2. Simulate sending that brief to Slack.
3. Simulate creating a Jira incident ticket.
4. Store both outbound actions in the `incident_actions` table.
5. Move the incident from `open` to `investigating`.

Example response shape:

```json
{
  "incident": {
    "id": 1,
    "status": "investigating",
    "title": "Checkout API latency spike"
  },
  "actions": [
    {
      "action_type": "slack_notification",
      "destination": "#sev-response",
      "external_reference": "mock-slack-abc123",
      "summary": "Sent incident brief to #sev-response..."
    },
    {
      "action_type": "jira_ticket",
      "destination": "INC",
      "external_reference": "INC-0001",
      "summary": "Created Jira incident ticket INC-0001..."
    }
  ]
}
```

## Example: view incident actions

Use:

```text
GET /incidents/{incident_id}/actions
```

This returns the audit trail of collaboration actions for the incident.

## Architecture

The core workflow is:

```text
Alert source
    ↓
FastAPI ingestion API
    ↓
Fingerprint service
    ↓
Duplicate incident check
    ↓
Mock log search + runbook retrieval
    ↓
AI-style incident analyzer
    ↓
Incident stored in SQLite
    ↓
Optional escalation
    ↓
Mock Slack/Jira integrations
    ↓
IncidentAction audit records
```

See [`docs/architecture.md`](docs/architecture.md) for system design details and production extension points.

## Commit history story

Recommended commit sequence:

```text
1. Initialize FastAPI incident copilot service
2. Add incident database model and API schemas
3. Implement incident ingestion and deduplication
4. Add AI incident analysis with logs and runbook context
5. Add tests, Docker support, and CI pipeline
6. Add incident escalation workflow with collaboration actions
```

## Future improvements

- Replace mock AI analyzer with OpenAI or Azure OpenAI
- Replace mock log search with Datadog, Splunk, CloudWatch, or OpenSearch
- Replace mock runbooks with Confluence, GitHub docs, Notion, or a vector database
- Replace mock Slack/Jira clients with real API integrations
- Add PostgreSQL support for production deployment
- Add authentication and role-based access control
- Add background workers for async enrichment and notifications
- Add Kubernetes manifests and Terraform infrastructure
- Add service-level dashboards and incident metrics

## Notes for GitHub cleanup

Do not commit generated local files such as:

```text
.venv/
.env
__pycache__/
.pytest_cache/
.ruff_cache/
*.pyc
incident_copilot.db
```

Make sure `.ruff_cache/` is included in `.gitignore` before pushing.
