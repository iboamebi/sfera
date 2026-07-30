"""
Add warehouse stock command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class AddStockCommand:
    """Add stock command."""

    stock_id: UUID
    warehouse_id: UUID
    material_id: UUID
    quantity: float
