"""
Warehouse movement repository interface.
"""

from abc import abstractmethod

from app.domains.warehouse.entities.warehouse_movement import (
    WarehouseMovement,
)
from app.shared.repositories.repository import Repository


class WarehouseMovementRepository(
    Repository[WarehouseMovement],
):
    """Warehouse movement repository interface."""

    @abstractmethod
    def save(
        self,
        movement: WarehouseMovement,
    ) -> None:
        """Save warehouse movement."""
