"""
Create order command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CreateOrderCommand:
    """Command for creating an order."""

    customer_id: UUID
    number: str
