"""
SQLAlchemy implementation of SiteRepository.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.domains.site.entities.site import Site
from app.domains.site.repositories.site_repository import SiteRepository
from app.infrastructure.mappers.site_mapper import SiteMapper
from app.models.site import Site as SiteModel


class SiteRepositorySQLAlchemy(SiteRepository):
    """SQLAlchemy repository for Site."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session
        self._mapper = SiteMapper()

    def get(
        self,
        site_id: UUID,
    ) -> Site | None:
        """Get site by identifier."""

        model = (
            self._session.query(SiteModel)
            .filter(
                SiteModel.id == site_id,
            )
            .first()
        )

        if model is None:
            return None

        return self._mapper.to_domain(model)

    def get_all(self) -> list[Site]:
        """Get all sites."""

        models = self._session.query(SiteModel).all()

        return [self._mapper.to_domain(model) for model in models]

    def get_by_organization_id(
        self,
        organization_id: UUID,
    ) -> list[Site]:
        """Get sites belonging to an organization."""

        models = (
            self._session.query(SiteModel)
            .filter(
                SiteModel.organization_id == organization_id,
            )
            .all()
        )

        return [self._mapper.to_domain(model) for model in models]

    def save(
        self,
        site: Site,
    ) -> Site:
        """Save site."""

        model = (
            self._session.query(SiteModel)
            .filter(
                SiteModel.id == site.id,
            )
            .first()
        )

        if model is None:
            model = SiteModel(
                id=site.id,
            )
            self._session.add(model)

        self._mapper.to_model(
            site,
            model,
        )

        self._session.flush()

        return self._mapper.to_domain(model)
