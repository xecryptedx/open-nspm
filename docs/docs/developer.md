# Developer Guide

## Prerequisites

- Python 3.11+
- Node.js 20+
- Docker & Docker Compose

## Setup

1. Create and activate a Python virtual environment.
2. Install backend dependencies: `pip install -r backend/requirements.txt`.
3. Install frontend dependencies: `cd frontend && npm install`.
4. Copy `.env.example` to `.env` and adjust secrets.

## Useful Commands

- `make dev` — build and run Docker services.
- `make fmt` — format code with Black and isort.
- `make lint` — run Ruff and mypy checks.
- `make test` — execute pytest suite.
- `make migrate` — apply latest Alembic migrations.

## Running Locally

```bash
export API_KEY=dev-api-key
export DATABASE_URL=sqlite:///./dev.db
uvicorn app.main:app --reload --app-dir backend
```

Visit `http://localhost:8000/v1/health` with the `x-api-key` header to verify the service.
