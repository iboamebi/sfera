from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PriceListItemBase(BaseModel):
    price_list_id: UUID
    name: str
    service_type: str | None = None
    unit_price: float


class PriceListItemCreate(PriceListItemBase):
    pass


class PriceListItemUpdate(BaseModel):
    name: str | None = None
    service_type: str | None = None
    unit_price: float | None = None


class PriceListItemRead(PriceListItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    archived: bool
