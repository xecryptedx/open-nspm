from .common import ORMBase, Timestamped


class TenantCreate(ORMBase):
    name: str


class TenantRead(Timestamped):
    id: int
    name: str
