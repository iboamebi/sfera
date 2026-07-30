from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CreateOrderCommand:
    order_id: UUID
    customer_id: UUID
    number: str
