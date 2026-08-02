"""
Warehouse stock domain entity.
"""

from dataclasses import dataclass
from uuid import UUID

from app.domains.warehouse.exceptions import (
    InsufficientReservedQuantityDomainError,
    InsufficientWarehouseStockDomainError,
    InvalidWarehouseQuantityDomainError,
)
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
            raise InvalidWarehouseQuantityDomainError

        if amount > available:
            raise InsufficientWarehouseStockDomainError

        self.reserved_quantity += amount

    def release(self, amount: float) -> None:
        """Release reserved quantity."""

        if amount <= 0:
            raise InvalidWarehouseQuantityDomainError

        if amount > self.reserved_quantity:
            raise InsufficientReservedQuantityDomainError

        self.reserved_quantity -= amount

    def add(self, amount: float) -> None:
        """Add material quantity."""

        if amount <= 0:
            raise InvalidWarehouseQuantityDomainError

        self.quantity += amount

    def remove(self, amount: float) -> None:
        """Remove material quantity."""

        available = self.quantity - self.reserved_quantity

        if amount <= 0:
            raise InvalidWarehouseQuantityDomainError

        if amount > available:
            raise InsufficientWarehouseStockDomainError

        self.quantity -= amount
