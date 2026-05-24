# AI Incident Copilot

AI Incident Copilot is a Python/FastAPI backend that simulates how a production-support or SRE team could triage incidents faster with alert deduplication, log context, runbook context, and AI-generated investigation guidance.

This repository is intentionally built in clear commit stages so reviewers can see the progression from a small service skeleton into a production-style backend.

## Current stage

**Commit 5: Tests, Docker support, CI, and architecture docs**

This stage adds the engineering polish expected in a serious GitHub portfolio project:

- Automated API tests with `pytest`
- Dockerfile for containerized execution
- Docker Compose for local container startup
- GitHub Actions CI pipeline
- Architecture documentation with a Mermaid diagram
- Ruff linting configuration

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
- Tests, Docker, and CI

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
│   │   └── incident.py
│   ├── schemas/
│   │   └── incident.py
│   ├── services/
│   │   ├── ai_analyzer.py
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

## Example alert ingestion request

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
  "symptoms": "...",
  "probable_cause": "...",
  "recommended_actions": ["..."],
  "postmortem_summary": "..."
}
```

## API endpoints

```text
GET  /health
POST /incidents/ingest
GET  /incidents
GET  /incidents/{incident_id}
POST /incidents/{incident_id}/resolve
```

## Architecture

See [`docs/architecture.md`](docs/architecture.md) for the system flow, layers, and production extension points.

## Future improvements

- Add a real OpenAI/Azure OpenAI analyzer implementation
- Add Datadog/Splunk/CloudWatch integrations
- Add Jira ticket creation
- Add Slack incident summaries
- Add PostgreSQL support for production deployment
- Add authentication and role-based access control
