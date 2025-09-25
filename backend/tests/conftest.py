import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("API_KEY", "testkey")

from app.main import app  # noqa: E402
from app.core import db  # noqa: E402
from app.models import Tenant  # noqa: E402


def _reset_database() -> None:
    db.Base.metadata.drop_all(bind=db.engine)
    db.Base.metadata.create_all(bind=db.engine)


@pytest.fixture(autouse=True)
def reset_db() -> Generator[None, None, None]:
    _reset_database()
    yield


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def api_headers() -> dict[str, str]:
    return {"x-api-key": os.environ["API_KEY"]}


@pytest.fixture()
def tenant_id() -> int:
    with db.SessionLocal() as session:
        tenant = Tenant(name="Test Tenant")
        session.add(tenant)
        session.commit()
        session.refresh(tenant)
        return tenant.id
