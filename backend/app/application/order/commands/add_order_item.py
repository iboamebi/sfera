from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class AddOrderItemCommand:
    order_id: UUID
    item_id: UUID
    instrument_id: UUID | None = None
