"""
SQLAlchemy implementation of OrganizationRepository.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.organization.entities.organization import Organization
from app.domains.organization.repositories.organization_repository import (
    OrganizationRepository,
)
from app.infrastructure.mappers.organization_mapper import OrganizationMapper
from app.models.organization import Organization as OrganizationModel


class OrganizationRepositorySQLAlchemy(OrganizationRepository):
    """SQLAlchemy repository for Organization."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session
        self._mapper = OrganizationMapper()

    def get(
        self,
        organization_id: UUID,
    ) -> Organization | None:
        model = (
            self._session.query(OrganizationModel)
            .filter(
                OrganizationModel.id == organization_id,
            )
            .first()
        )

        if model is None:
            return None

        return self._mapper.to_domain(model)

    def get_all(self) -> list[Organization]:
        models = self._session.query(OrganizationModel).all()

        return [self._mapper.to_domain(model) for model in models]

    def save(
        self,
        organization: Organization,
    ) -> Organization:
        model = (
            self._session.query(OrganizationModel)
            .filter(
                OrganizationModel.id == organization.id,
            )
            .first()
        )

        if model is None:
            model = OrganizationModel(
                id=organization.id,
            )
            self._session.add(model)

        self._mapper.to_model(
            organization,
            model,
        )

        self._session.flush()

        return self._mapper.to_domain(model)
