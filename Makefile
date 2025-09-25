.PHONY: dev fmt lint test migrate seed

DEV_COMPOSE = docker-compose -f deploy/docker-compose.yml

fmt:
black backend
isort backend

lint:
ruff check backend
mypy backend/app

dev:
$(DEV_COMPOSE) up --build

test:
pytest --maxfail=1 --disable-warnings

migrate:
cd backend && alembic upgrade head

seed:
python scripts/seed.py
