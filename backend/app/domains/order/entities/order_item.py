from dataclasses import dataclass, field
from uuid import UUID

from app.domains.order.exceptions.order_exception import OrderException
from app.domains.order.value_objects.order_item_operation import OrderItemOperation
from app.shared.base.entity import Entity


@dataclass(eq=False, kw_only=True)
class OrderItem(Entity):
    """One measuring instrument or instrument type in an order."""

    instrument_id: UUID | None = None
    instrument_type_id: UUID | None = None
    quantity: int = 1
    customer_inventory_number: str | None = None
    comment: str | None = None
    requested_operations: set[OrderItemOperation] = field(default_factory=set)

    def __post_init__(self) -> None:
        """Validate order item invariants."""
        if self.quantity < 1:
            raise OrderException("Order item quantity must be at least one")
