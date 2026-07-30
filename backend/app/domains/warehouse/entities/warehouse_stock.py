"""
Warehouse stock domain entity.
"""

from dataclasses import dataclass
from uuid import UUID

from app.shared.base.entity import Entity


@dataclass(eq=False)
class WarehouseStock(Entity):
    """Warehouse stock entity."""

    warehouse_id: UUID
    material_id: UUID
    quantity: float = 0
    reserved_quantity: float = 0

    def reserve(self, amount: float) -> None:
        """Reserve material quantity."""

        available = self.quantity - self.reserved_quantity

        if amount <= 0:
            raise ValueError("Reserve amount must be positive")

        if amount > available:
            raise ValueError("Insufficient available quantity")

        self.reserved_quantity += amount

    def release(self, amount: float) -> None:
        """Release reserved material quantity."""

        if amount <= 0:
            raise ValueError("Release amount must be positive")

        if amount > self.reserved_quantity:
            raise ValueError("Release amount exceeds reserved quantity")

        self.reserved_quantity -= amount

    def add(self, amount: float) -> None:
        """Add material quantity."""

        if amount <= 0:
            raise ValueError("Quantity must be positive")

        self.quantity += amount

    def remove(self, amount: float) -> None:
        """Remove material quantity."""

        available = self.quantity - self.reserved_quantity

        if amount <= 0:
            raise ValueError("Quantity must be positive")

        if amount > available:
            raise ValueError("Insufficient stock quantity")

        self.quantity -= amount
