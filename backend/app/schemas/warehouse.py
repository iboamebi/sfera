from uuid import UUID

from pydantic import BaseModel, ConfigDict


class WarehouseBase(BaseModel):
    name: str
    address: str | None = None
    responsible_person: str | None = None
    comment: str | None = None


class WarehouseCreate(WarehouseBase):
    pass


class WarehouseUpdate(BaseModel):
    name: str | None = None
    address: str | None = None
    responsible_person: str | None = None
    comment: str | None = None


class WarehouseRead(WarehouseBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    archived: bool
