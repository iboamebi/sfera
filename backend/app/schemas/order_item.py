from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OrderItemBase(BaseModel):
    order_id: UUID
    instrument_id: UUID | None = None
    line_number: int
    customer_inventory_number: str | None = None
    customer_comment: str | None = None


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemUpdate(BaseModel):
    instrument_id: UUID | None = None
    line_number: int | None = None
    customer_inventory_number: str | None = None
    customer_comment: str | None = None


class OrderItemRead(OrderItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    archived: bool
