# API Overview

All API endpoints are prefixed with `/v1` and require an `x-api-key` header.

## Health

- `GET /v1/health` — returns `{ "status": "ok" }` when the service is healthy.

## Devices

- `POST /v1/devices` — register a device for a tenant.
- `GET /v1/devices` — list registered devices.
- `GET /v1/devices/{id}` — retrieve a device by identifier.

## Snapshots

- `POST /v1/snapshots:upload` — upload a FortiGate configuration export (multipart form) and create a snapshot.
- `GET /v1/snapshots` — list snapshots (filterable by `device_id`).
- `GET /v1/snapshots/{id}` — get snapshot metadata.

## Findings

- `POST /v1/findings:run` — run hygiene checks against a snapshot.
- `GET /v1/findings` — list findings (filterable by `snapshot_id`).

## Diffs

- `POST /v1/diffs` — compute a diff between snapshots.
- `GET /v1/diffs/{id}` — retrieve a diff record.

## Reports

- `GET /v1/reports/{snapshot_id}.html` — render a snapshot report as HTML.
