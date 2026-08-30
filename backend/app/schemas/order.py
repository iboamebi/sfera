"""
Order API schemas.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.domains.order.value_objects.order_item_operation import OrderItemOperation
from app.domains.order.value_objects.order_number import OrderNumber
from app.domains.order.value_objects.order_status import OrderStatus


class OrderCreate(BaseModel):
    """Create order request."""

    number: str
    customer_id: UUID
    planned_issue_at: datetime | None = None
    comment: str | None = None


class OrderUpdate(BaseModel):
    """Update order request."""

    planned_issue_at: datetime | None = None
    comment: str | None = None


class OrderItemRead(BaseModel):
    """Order item response."""

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    instrument_id: UUID | None = None
    instrument_type_id: UUID | None = None
    instrument_type_name: str | None = None
    instrument_type_model: str | None = None
    instrument_type_measurement_type: str | None = None
    serial_number: str | None = None
    registry_number: str | None = None
    modification: str | None = None
    factory_number: str | None = None
    manufacture_year: int | None = None
    inventory_number: str | None = None
    comment: str | None = None
    requested_operations: list[OrderItemOperation] = Field(default_factory=list)


class OrderRead(BaseModel):
    """Order response."""

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    number: str
    customer_id: UUID
    status: OrderStatus
    received_at: datetime
    planned_issue_at: datetime | None = None
    issued_at: datetime | None = None
    comment: str | None = None
    archived: bool
    items: list[OrderItemRead] = Field(default_factory=list)

    @field_validator("number", mode="before")
    @classmethod
    def serialize_order_number(cls, value: str | OrderNumber) -> str:
        """Convert the domain value object to the API string contract."""
        if isinstance(value, OrderNumber):
            return value.value
        return value
