"""
Customer-Organization association repository interface.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from app.domains.organization.entities.organization import Organization


class CustomerOrganizationRepository(ABC):
    """Abstract repository for Customer ↔ Organization links."""

    @abstractmethod
    def get_organizations(self, customer_id: UUID) -> list[Organization]:
        """Get organizations linked to a customer."""

        raise NotImplementedError

    @abstractmethod
    def add(self, customer_id: UUID, organization_id: UUID) -> None:
        """Link an organization to a customer."""

        raise NotImplementedError

    @abstractmethod
    def remove(self, customer_id: UUID, organization_id: UUID) -> None:
        """Remove an organization link from a customer."""

        raise NotImplementedError
