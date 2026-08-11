"""
Price list item API schemas.

Defines HTTP contracts for price list item operations.
Version: 2.0
Revision: 2026-08-11
"""

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PriceListItemBase(BaseModel):
    """Common fields for price list item creation and reading."""

    price_list_id: UUID
    service_code: str
    name: str
    price: Decimal
    unit: str = "pcs"
    description: str | None = None


class PriceListItemCreate(PriceListItemBase):
    """Request schema for creating a price list item."""


class PriceListItemUpdate(BaseModel):
    """Request schema for updating mutable price list item fields."""

    price: Decimal | None = None
    description: str | None = None


class PriceListItemRead(PriceListItemBase):
    """Response schema for a price list item."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    archived: bool
