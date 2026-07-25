"""
Application service: Organization.
"""

from uuid import UUID

from app.domains.organization.entities.organization import Organization
from app.domains.organization.repositories.organization_repository import (
    OrganizationRepository,
)


class OrganizationApplicationService:
    """Organization application service."""

    def __init__(
        self,
        repository: OrganizationRepository,
    ) -> None:
        self._repository = repository

    def get(
        self,
        organization_id: UUID,
    ) -> Organization:
        """Get organization by identifier."""

        organization = self._repository.get(
            organization_id,
        )

        if organization is None:
            raise ValueError("Organization not found")

        return organization

    def get_all(self) -> list[Organization]:
        """Get all organizations."""

        return self._repository.get_all()

    def save(
        self,
        organization: Organization,
    ) -> Organization:
        """Save organization."""

        return self._repository.save(
            organization,
        )
