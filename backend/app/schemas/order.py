from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.order import OrderStatus


class OrderBase(BaseModel):
    number: str
    customer_id: UUID
    status: OrderStatus = OrderStatus.NEW
    received_at: datetime
    planned_issue_at: datetime | None = None
    issued_at: datetime | None = None
    comment: str | None = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    number: str | None = None
    customer_id: UUID | None = None
    status: OrderStatus | None = None
    received_at: datetime | None = None
    planned_issue_at: datetime | None = None
    issued_at: datetime | None = None
    comment: str | None = None


class OrderRead(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    archived: bool
