from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from .config import settings


class Base(DeclarativeBase):
    pass


def _create_engine():
    connect_args = {}
    if settings.database_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
    return create_engine(settings.database_url, echo=False, future=True, connect_args=connect_args)


def _create_session_factory(engine):
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, class_=Session)


def get_engine():
    return _create_engine()


engine = get_engine()
SessionLocal = _create_session_factory(engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
