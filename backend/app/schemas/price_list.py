from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PriceListBase(BaseModel):
    name: str
    description: str | None = None
    is_active: bool = True


class PriceListCreate(PriceListBase):
    pass


class PriceListUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class PriceListRead(PriceListBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    archived: bool
