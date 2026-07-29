# adder-app

A minimal FastAPI service that adds two numbers — built as a full, industry-standard
software engineering exercise: design, testing, containerization, CI/CD, and deployment.

## Architecture

```
Browser (htmx form) ──┐
├──▶ FastAPI ──▶ core.add()
JSON API clients ──────┘ │
├──▶ structlog (JSON logs)
├──▶ slowapi (rate limiting)
└──▶ CORS middleware

FastAPI ──▶ Docker image ──▶ GHCR ──▶ Railway (auto-redeploy on new :latest)
```

- **`app/core.py`** — pure business logic, framework-agnostic
- **`app/schemas.py`** — Pydantic request/response contracts
- **`app/config.py`** — environment-driven settings (pydantic-settings)
- **`app/logging_config.py`** — structured JSON logging setup
- **`app/main.py`** — FastAPI routes, middleware, wiring
- **`app/templates/`** — Jinja2 + htmx frontend

## Known Limitations

- Rate limiting uses in-memory storage — resets on restart, and won't work
  correctly across multiple replicas (would need Redis-backed storage for that)
- Values that overflow float precision (e.g. very large number additions)
  serialize to `null` in the JSON response rather than an explicit error
- No authentication — this is intentionally a public, stateless calculator API

## Tech Stack

- **Backend**: Python 3.12, FastAPI, Pydantic
- **Frontend**: htmx, Tailwind CSS (CDN), Jinja2
- **Package management**: uv
- **Testing**: pytest
- **Linting/type-checking**: ruff, mypy
- **Containerization**: Docker, Docker Compose
- **Observability**: structlog (structured JSON logging)
- **Resilience**: slowapi (rate limiting), CORS middleware
- **CI/CD**: GitHub Actions → GHCR → Railway

## Getting Started

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

### Setup

Clone the repo, then install dependencies:

```bash
uv sync
```

This creates a `.venv` and installs everything from `pyproject.toml` / `uv.lock`.

### Running locally

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.
Interactive API docs: `http://127.0.0.1:8000/docs`

### Running tests

```bash
uv run pytest -v
```

### Linting and type-checking

```bash
uv run ruff check .
uv run mypy .
```

### Running with Docker

Build and run the container directly:

```bash
docker build -t adder-app .
docker run -p 8000:8000 --env-file .env adder-app
```

Or use Docker Compose (recommended for local dev):

```bash
docker compose up --build
```

This builds the image and starts the service at `http://127.0.0.1:8000`, using
`.env` for configuration. Stop it with:

```bash
docker compose down
```

The container exposes a `/health` endpoint used by Docker's built-in healthcheck
to confirm the service is responsive.

## Deployment

This project deploys automatically via CI/CD:

1. On every push to `master`, GitHub Actions runs linting, type-checking, and tests
2. If those pass, a Docker image is built and pushed to GitHub Container Registry
   (`ghcr.io/ksdfjklj/adder-app`), tagged with both the commit SHA and `latest`
3. GitHub Actions then triggers a redeploy on Railway, which pulls the freshly
   pushed image and runs it

No manual deployment steps are required — pushing to `master` is the only
trigger needed, provided all checks pass.

**Live URL**: https://adder-app-production.up.railway.app/

### Infrastructure

- **Registry**: GitHub Container Registry (GHCR)
- **Hosting**: [Railway](https://railway.com)
- **Trigger**: GitHub Actions workflow (`.github/workflows/ci.yml`)

## API Reference

### `GET /health`

Health check — confirms the service is up.

**Response** `200 OK`
```json
{"status": "ok"}
```

### `POST /add`

Adds two numbers.

**Request body**
```json
{"a": 2, "b": 3}
```

**Response** `200 OK`
```json
{"result": 5.0}
```

**Response** `422 Unprocessable Entity` — if `a` or `b` is missing or not a number.

## Project Status

🚧 In progress — see commit history for build order and reasoning.