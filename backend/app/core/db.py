from __future__ import annotations

from collections.abc import Generator
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Type


class Metadata:
    def create_all(self, bind: "InMemoryEngine") -> None:  # noqa: F821
        bind.create_all()

    def drop_all(self, bind: "InMemoryEngine") -> None:  # noqa: F821
        bind.drop_all()


class BaseModel:
    __tablename__: str

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            elif isinstance(value, list):
                result[key] = [self._serialize(item) for item in value]
            elif isinstance(value, dict):
                result[key] = {
                    sub_key: self._serialize(sub_value)
                    for sub_key, sub_value in value.items()
                }
            else:
                result[key] = self._serialize(value)
        return result

    @staticmethod
    def _serialize(value: Any) -> Any:
        if isinstance(value, datetime):
            return value.isoformat()
        return value


class Base:
    metadata = Metadata()


@dataclass
class InMemoryEngine:
    factories: dict[str, Callable[[], BaseModel]] = field(default_factory=dict)
    storage: dict[str, dict[int, BaseModel]] = field(default_factory=dict)
    sequences: dict[str, int] = field(default_factory=dict)

    def register_model(self, name: str, factory: Callable[[], BaseModel]) -> None:
        self.factories[name] = factory
        self.storage.setdefault(name, {})
        self.sequences.setdefault(name, 1)

    def create_all(self) -> None:
        for name in self.factories:
            self.storage.setdefault(name, {})
            self.sequences.setdefault(name, 1)

    def drop_all(self) -> None:
        for table in self.storage.values():
            table.clear()
        for key in self.sequences:
            self.sequences[key] = 1


class Session:
    def __init__(self, engine: InMemoryEngine):
        self.engine = engine

    def add(self, instance: BaseModel) -> None:
        table = self.engine.storage.setdefault(instance.__tablename__, {})
        if getattr(instance, "id", None) is None:
            next_id = self.engine.sequences.setdefault(instance.__tablename__, 1)
            setattr(instance, "id", next_id)
            self.engine.sequences[instance.__tablename__] = next_id + 1
        table[instance.id] = instance

    def add_all(self, instances: list[BaseModel]) -> None:
        for item in instances:
            self.add(item)

    def delete(self, instance: BaseModel) -> None:
        table = self.engine.storage.get(instance.__tablename__, {})
        table.pop(getattr(instance, "id", 0), None)

    def commit(self) -> None:
        return None

    def refresh(self, instance: BaseModel) -> None:
        return None

    def get(self, model: Type[BaseModel], obj_id: int) -> BaseModel | None:
        table = self.engine.storage.get(model.__tablename__, {})
        return table.get(obj_id)

    def query(self, model: Type[BaseModel]) -> "Query":
        return Query(self, model)

    def close(self) -> None:
        return None


class Query:
    def __init__(self, session: Session, model: Type[BaseModel]):
        self.session = session
        self.model = model
        self._data = list(session.engine.storage.get(model.__tablename__, {}).values())

    def _clone(self, data: list[BaseModel]) -> "Query":
        clone = Query(self.session, self.model)
        clone._data = data
        return clone

    def filter(self, predicate: Callable[[BaseModel], bool]) -> "Query":
        return self._clone([item for item in self._data if predicate(item)])

    def order_by(self, key: Callable[[BaseModel], Any], *, reverse: bool = False) -> "Query":
        return self._clone(sorted(self._data, key=key, reverse=reverse))

    def first(self) -> BaseModel | None:
        return self._data[0] if self._data else None

    def all(self) -> list[BaseModel]:
        return list(self._data)


engine = InMemoryEngine()


def SessionLocal() -> Session:
    return Session(engine)


def get_db() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
