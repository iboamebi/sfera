from dataclasses import dataclass, field
from uuid import UUID

from app.domains.order.value_objects.order_item_operation import OrderItemOperation
from app.shared.base.entity import Entity


@dataclass(eq=False, kw_only=True)
class OrderItem(Entity):
    """One measuring instrument type or concrete instrument in an order."""

    instrument_type_id: UUID | None = None
    instrument_id: UUID | None = None
    comment: str | None = None
    requested_operations: set[OrderItemOperation] = field(default_factory=set)
