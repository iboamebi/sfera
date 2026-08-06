from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PriceListBase(BaseModel):
    name: str
    price_list_type: str
    currency: str = "RUB"
    description: str | None = None
    valid_from: date | None = None
    valid_to: date | None = None
    is_active: bool = True


class PriceListCreate(PriceListBase):
    pass


class PriceListUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None
    valid_from: date | None = None
    valid_to: date | None = None


class PriceListRead(PriceListBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    archived: bool
