# app/schemas/price_list.py
# PriceList API schemas.

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PriceListBase(BaseModel):
    """
    Base schema for PriceList.
    """

    name: str
    price_list_type: str
    currency: str = "RUB"
    description: str | None = None
    valid_from: date | None = None
    valid_to: date | None = None
    is_active: bool = True


class PriceListCreate(PriceListBase):
    """
    Schema for creating PriceList.
    """

    pass


class PriceListUpdate(BaseModel):
    """
    Schema for updating PriceList.
    """

    name: str | None = None
    price_list_type: str | None = None
    currency: str | None = None
    description: str | None = None
    is_active: bool | None = None
    valid_from: date | None = None
    valid_to: date | None = None


class PriceListRead(PriceListBase):
    """
    Schema for reading PriceList.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    archived: bool
