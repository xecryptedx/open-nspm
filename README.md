# OpenNSPM

OpenNSPM is an open-source Network Security Policy Management (NSPM) platform focused on Fortinet FortiGate/FortiManager support. This repository provides the initial MVP backend, worker, and frontend scaffolding needed to ingest firewall configurations, normalize policy data, run hygiene checks, and generate reports.

## Quickstart

```bash
# Clone the repository
 git clone https://github.com/your-org/open-nspm.git
 cd open-nspm

# Start the full stack
make dev
```

Docker Compose builds the backend API, PostgreSQL database, Redis, and worker. Once the containers are healthy, verify the API:

```bash
curl -H "x-api-key: dev-api-key" http://localhost:8000/v1/health
```

Expected response:

```json
{"status": "ok"}
```

## Configuration

Environment variables are read via [`app/core/config.py`](backend/app/core/config.py). Copy `deploy/.env.example` to `.env` to customize credentials and API keys.

Key variables:

- `API_KEY` — shared secret for FastAPI endpoints (default: `dev-api-key`).
- `DATABASE_URL` — SQLAlchemy URL for PostgreSQL (default points to the Compose service).
- `REDIS_URL` — Redis connection string for background tasks.
- `FORTI_VERIFY_SSL` — toggle SSL verification for Fortinet API requests.

## Development Workflow

- `make fmt` — format backend code with Black and isort.
- `make lint` — run Ruff and mypy checks.
- `make test` — execute the pytest suite.
- `make migrate` — apply Alembic migrations to the configured database.

The FastAPI application lives under [`backend/app`](backend/app). Run the API locally without Docker using:

```bash
export API_KEY=dev-api-key
export DATABASE_URL=sqlite:///./dev.db
uvicorn app.main:app --reload --app-dir backend
```

The frontend (React + Vite + Tailwind) is located under [`frontend`](frontend). Start it with `npm run dev` after installing dependencies.

## Documentation

MkDocs documentation is located in the `docs` directory. Build the site locally with:

```bash
pip install mkdocs-material
mkdocs serve
```

## Testing

Pytest fixtures spin up an in-memory SQLite database. Integration tests cover device CRUD, snapshot ingestion, hygiene detection, and report rendering. Run tests via `make test`.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
