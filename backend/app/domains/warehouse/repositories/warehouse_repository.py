"""
Warehouse repository interface.
"""

from abc import abstractmethod
from uuid import UUID

from app.domains.warehouse.entities.warehouse import Warehouse
from app.shared.repositories.repository import Repository


class WarehouseRepository(
    Repository[Warehouse],
):
    """Warehouse repository interface."""

    @abstractmethod
    def get(
        self,
        warehouse_id: UUID,
    ) -> Warehouse | None:
        """Get warehouse by id."""

    @abstractmethod
    def save(
        self,
        warehouse: Warehouse,
    ) -> None:
        """Save warehouse."""
