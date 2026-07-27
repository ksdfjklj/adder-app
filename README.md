# adder-app

A minimal FastAPI service that adds two numbers — built as a full, industry-standard
software engineering exercise: design, testing, containerization, CI/CD, and deployment.

## Tech Stack

- **Backend**: Python 3.11, FastAPI, Pydantic
- **Package management**: uv
- **Testing**: pytest
- **Linting/type-checking**: ruff, mypy

## Getting Started

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

### Setup

Clone the repo, then install dependencies:

\```bash
uv sync
\```

This creates a `.venv` and installs everything from `pyproject.toml` / `uv.lock`.

### Running locally

\```bash
uv run uvicorn app.main:app --reload
\```

The API will be available at `http://127.0.0.1:8000`.
Interactive API docs: `http://127.0.0.1:8000/docs`

### Running tests

\```bash
uv run pytest -v
\```

### Linting and type-checking

\```bash
uv run ruff check .
uv run mypy .
\```

## API Reference

### `GET /health`

Health check — confirms the service is up.

**Response** `200 OK`
\```json
{"status": "ok"}
\```

### `POST /add`

Adds two numbers.

**Request body**
\```json
{"a": 2, "b": 3}
\```

**Response** `200 OK`
\```json
{"result": 5.0}
\```

**Response** `422 Unprocessable Entity` — if `a` or `b` is missing or not a number.

## Project Status

🚧 In progress — see commit history for build order and reasoning.