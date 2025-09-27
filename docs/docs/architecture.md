# Architecture

OpenNSPM follows a service-oriented layout with a FastAPI backend, React frontend, and background worker queue.

## Backend

- **FastAPI** application under `backend/app` exposes REST endpoints secured by API key.
- **SQLAlchemy** models map to PostgreSQL tables for tenants, devices, snapshots, findings, and diffs.
- **Alembic** migrations manage schema changes (`backend/migrations`).
- **Services** encapsulate integrations, normalization, hygiene checks, and diffing.
- **Reports** generate HTML summaries for human consumption.

## Worker

A lightweight worker container is provided for future Dramatiq/RQ integration. The current iteration persists collected payloads by calling service helpers.

## Frontend

The React + Vite + Tailwind frontend renders a minimal dashboard and queries the FastAPI health endpoint to display connectivity status.

## Infrastructure

Docker Compose orchestrates the backend API, PostgreSQL database, Redis cache, and worker. Environment variables are supplied via `.env` files or Compose overrides.
