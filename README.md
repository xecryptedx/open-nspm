# OpenNSPM (lightweight prototype)

OpenNSPM is an experiment in modeling the core workflows of a Network Security Policy Management (NSPM) platform focused on Fortinet FortiGate / FortiManager devices. This repository contains a fully testable Python implementation that can be executed without third-party dependencies or network access. The current iteration emphasises:

* an HTTP-style API surface implemented with a small self-contained FastAPI-compatible shim;
* an in-memory persistence layer that mimics relational database semantics;
* snapshot normalisation, hygiene analysis, and HTML reporting helpers; and
* a pytest suite that exercises device registration, snapshot ingestion, hygiene checks, diffing, and reporting.

The goal of this deliverable is to explain and demonstrate how the application behaves today while remaining runnable inside restricted sandboxes.

## What works right now?

* **Device CRUD** – `POST /v1/devices`, `GET /v1/devices`, and `GET /v1/devices/{id}` manage devices inside an in-memory catalogue keyed by tenant.
* **Snapshot uploads** – `POST /v1/snapshots:upload` accepts FortiGate configuration text, parses policy and address blocks, normalises them, and stores the result in memory.
* **Findings** – `POST /v1/findings:run` evaluates any-any and disabled-rule hygiene checks and persists findings for later retrieval via `GET /v1/findings`.
* **Diffs** – `POST /v1/diffs` compares two snapshots using the lightweight diff engine and exposes the stored result through `GET /v1/diffs/{id}`.
* **Reports** – `GET /v1/reports/{snapshot_id}.html` renders a Tailwind-styled HTML summary including snapshot metadata, findings, and diff counts.
* **Health endpoint** – `GET /v1/health` returns a static `{"status": "ok"}` payload and is used by the tests to validate the application wiring.

All endpoints enforce an API key via the custom `fastapi` shim. The key defaults to `dev-api-key` but can be overridden by setting the `API_KEY` environment variable.

## Running the test suite

The repository ships with an embedded FastAPI-compatible implementation, an in-memory data store, and zero external dependencies. The only requirement is Python 3.11 or newer. Execute the test suite from the repository root:

```bash
pytest
```

The tests seed tenants, exercise the HTTP routes through the shim `TestClient`, and confirm that the normaliser, hygiene engine, and report generator behave as expected.

## Interacting programmatically

You can explore the API in a REPL without starting an HTTP server by using the bundled `TestClient`:

```bash
PYTHONPATH=backend:. python - <<'PY'
from fastapi.testclient import TestClient
from app.main import app
from app.core import db
from app.models import Tenant

session = db.SessionLocal()
tenant = Tenant(name="Example Tenant")
session.add(tenant)
session.commit()
session.refresh(tenant)

client = TestClient(app)
headers = {"x-api-key": "dev-api-key"}

# Register a device
resp = client.post(
    "/v1/devices",
    json={"tenant_id": tenant.id, "hostname": "edge-fw"},
    headers=headers,
)
print(resp.json())

device_id = resp.json()["id"]

# Upload a FortiGate snapshot from the bundled fixture
from pathlib import Path
payload = Path("backend/tests/fixtures/sample_fortigate.conf").read_bytes()
resp = client.post(
    "/v1/snapshots:upload",
    headers=headers,
    data={"device_id": str(device_id)},
    files={"file": ("config.txt", payload, "text/plain")},
)
print(resp.json()["normalized_json"].keys())
PY
```

## Project layout

```
backend/app/
  core/          # in-memory DB, config, security helpers
  api/v1/        # HTTP-style routes
  models/        # dataclass-backed persistence entities
  services/      # normaliser, hygiene, diff, and Fortinet stubs
  importers/     # FortiGate text parser
  reports/       # HTML report renderer
  workers/       # snapshot pull task skeleton
backend/tests/   # pytest suite and FortiGate fixture
fastapi/         # minimal FastAPI/TestClient compatibility layer
```

## Configuration knobs

The in-memory runtime reads a handful of environment variables (see `backend/app/core/config.py`):

* `API_KEY` – API key expected in the `x-api-key` header (default `dev-api-key`).
* `DATABASE_URL`, `REDIS_URL`, `FORTI_VERIFY_SSL` – accepted for compatibility; unused in the in-memory prototype but preserved for forward evolution.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
