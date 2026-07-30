"""
Release warehouse stock command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ReleaseStockCommand:
    """Release stock command."""

    warehouse_id: UUID
    material_id: UUID
    quantity: float
    order_id: UUID | None = None
