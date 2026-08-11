"""
Add warehouse stock command.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class AddStockCommand:
    """Add stock command."""

    warehouse_id: UUID
    material_id: UUID
    quantity: float
