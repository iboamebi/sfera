"""Assign an instrument to an order item command."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class AssignOrderItemInstrumentCommand:
    """Command for assigning a concrete instrument to an order item."""

    order_id: UUID
    item_id: UUID
    instrument_id: UUID
