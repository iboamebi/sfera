"""
Material repository interface.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from app.domains.material.entities.material import Material


class MaterialRepository(ABC):
    """Abstract material repository."""

    @abstractmethod
    def get(
        self,
        material_id: UUID,
    ) -> Material | None:
        """Get material by identifier."""

        raise NotImplementedError

    @abstractmethod
    def get_all(
        self,
    ) -> list[Material]:
        """Get all materials."""

        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        material: Material,
    ) -> Material:
        """Save material."""

        raise NotImplementedError
