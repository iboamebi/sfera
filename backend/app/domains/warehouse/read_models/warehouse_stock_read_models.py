"""
Warehouse stock read models.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, kw_only=True)
class WarehouseStockReadData:
    """Read model for warehouse stock."""

    id: UUID
    warehouse_id: UUID
    warehouse_name: str
    material_id: UUID
    material_name: str
    quantity: float
    reserved_quantity: float
    available_quantity: float
