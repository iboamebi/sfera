"""
Organization repository interface.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from app.domains.organization.entities.organization import Organization


class OrganizationRepository(ABC):
    """Abstract organization repository."""

    @abstractmethod
    def get(
        self,
        organization_id: UUID,
    ) -> Organization | None:
        """Get organization by identifier."""

        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[Organization]:
        """Get all organizations."""

        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        organization: Organization,
    ) -> Organization:
        """Save organization."""

        raise NotImplementedError
