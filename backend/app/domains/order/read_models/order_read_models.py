"""
Order read models.
"""

from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID

from app.domains.order.value_objects.order_item_operation import OrderItemOperation
from app.domains.order.value_objects.order_status import OrderStatus
from app.domains.verification.value_objects.verification_result import (
    VerificationResult,
)
from app.domains.verification.value_objects.verification_status import (
    VerificationStatus,
)
from app.domains.verification.value_objects.verification_type import VerificationType


@dataclass(frozen=True)
class OrderItemVerificationReadData:
    """Verification summary exposed as part of an order item."""

    id: UUID
    created_at: datetime
    verification_date: date
    verification_type: VerificationType
    status: VerificationStatus
    result: VerificationResult | None
    valid_until: date | None
    archived: bool


@dataclass(frozen=True)
class OrderItemReadData:
    """Order item read data."""

    id: UUID
    instrument_id: UUID | None
    instrument_type_id: UUID | None
    instrument_name: str | None
    instrument_type_name: str | None
    serial_number: str | None
    modification: str | None
    comment: str | None
    requested_operations: set[OrderItemOperation]
    verification_ids: list[UUID]
    verifications: list[OrderItemVerificationReadData]


@dataclass(frozen=True)
class OrderReadData:
    """Order read data."""

    id: UUID
    number: str
    customer_id: UUID
    customer_name: str
    status: OrderStatus
    received_at: datetime
    created_at: datetime
    updated_at: datetime
    planned_issue_at: datetime | None
    issued_at: datetime | None
    comment: str | None
    archived: bool
    items: list[OrderItemReadData]
