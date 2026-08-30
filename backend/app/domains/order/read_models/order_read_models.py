"""
Order read models.
"""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domains.order.value_objects.order_item_operation import OrderItemOperation
from app.domains.order.value_objects.order_status import OrderStatus


@dataclass(frozen=True)
class OrderItemReadData:
    """Order item read data."""

    id: UUID
    instrument_id: UUID | None
    instrument_type_id: UUID | None
    instrument_type_name: str | None
    instrument_type_model: str | None
    instrument_type_measurement_type: str | None
    serial_number: str | None
    modification: str | None
    comment: str | None
    requested_operations: set[OrderItemOperation]


@dataclass(frozen=True)
class OrderReadData:
    """Order read data."""

    id: UUID
    number: str
    customer_id: UUID
    status: OrderStatus
    received_at: datetime
    planned_issue_at: datetime | None
    issued_at: datetime | None
    comment: str | None
    archived: bool
    items: list[OrderItemReadData]
