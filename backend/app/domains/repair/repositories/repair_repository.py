"""
Repair repository interface.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from app.domains.repair.entities.repair import Repair


class RepairRepository(ABC):
    """Repository contract for repairs."""

    @abstractmethod
    def get(
        self,
        repair_id: UUID,
    ) -> Repair | None:
        """Get repair by id."""

        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        repair: Repair,
    ) -> None:
        """Save repair."""

        raise NotImplementedError
