"""
SQLAlchemy implementation of Customer ↔ Organization association repository.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.customer.repositories.customer_organization_repository import (
    CustomerOrganizationRepository,
)
from app.domains.organization.entities.organization import Organization
from app.infrastructure.mappers.organization_mapper import OrganizationMapper
from app.models.customer_organization import CustomerOrganization
from app.models.organization import Organization as OrganizationModel


class CustomerOrganizationRepositorySQLAlchemy(CustomerOrganizationRepository):
    """SQLAlchemy repository for Customer ↔ Organization links."""

    def __init__(self, session: Session) -> None:
        self._session = session
        self._organization_mapper = OrganizationMapper()

    def get_organizations(self, customer_id: UUID) -> list[Organization]:
        models = (
            self._session.query(OrganizationModel)
            .join(
                CustomerOrganization,
                CustomerOrganization.organization_id
                == OrganizationModel.id,
            )
            .filter(
                CustomerOrganization.customer_id == customer_id,
                CustomerOrganization.archived.is_(False),
            )
            .order_by(OrganizationModel.name)
            .all()
        )

        return [self._organization_mapper.to_domain(model) for model in models]

    def add(self, customer_id: UUID, organization_id: UUID) -> None:
        link = (
            self._session.query(CustomerOrganization)
            .filter(
                CustomerOrganization.customer_id == customer_id,
                CustomerOrganization.organization_id == organization_id,
            )
            .first()
        )

        if link is None:
            self._session.add(
                CustomerOrganization(
                    customer_id=customer_id,
                    organization_id=organization_id,
                )
            )
        elif link.archived:
            link.archived = False

        self._session.flush()

    def remove(self, customer_id: UUID, organization_id: UUID) -> None:
        link = (
            self._session.query(CustomerOrganization)
            .filter(
                CustomerOrganization.customer_id == customer_id,
                CustomerOrganization.organization_id == organization_id,
                CustomerOrganization.archived.is_(False),
            )
            .first()
        )

        if link is None:
            return

        link.archived = True
        self._session.flush()
