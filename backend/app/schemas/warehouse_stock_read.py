"""
Warehouse stock read schemas.
"""

from uuid import UUID

from pydantic import BaseModel


class WarehouseStockRead(BaseModel):
    """Warehouse stock response."""

    id: UUID
    warehouse_id: UUID
    warehouse_name: str
    material_id: UUID
    material_name: str
    quantity: float
    reserved_quantity: float
    available_quantity: float
