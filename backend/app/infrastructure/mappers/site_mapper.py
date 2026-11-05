"""
Site domain/model mapper.
"""

from app.domains.site.entities.site import Site
from app.infrastructure.mappers.base_mapper import BaseMapper
from app.models.site import Site as SiteModel


class SiteMapper(
    BaseMapper[
        Site,
        SiteModel,
    ],
):
    """Maps Site between domain and SQLAlchemy model."""

    def to_domain(
        self,
        model: SiteModel,
    ) -> Site:
        """Convert ORM model to domain entity."""

        return Site(
            id=model.id,
            customer_id=model.customer_id,
            name=model.name,
            address=model.address,
            archived=model.archived,
        )

    def to_model(
        self,
        entity: Site,
        model: SiteModel,
    ) -> SiteModel:
        """Convert domain entity to ORM model."""

        model.customer_id = entity.customer_id
        model.name = entity.name
        model.address = entity.address
        model.archived = entity.archived

        return model
