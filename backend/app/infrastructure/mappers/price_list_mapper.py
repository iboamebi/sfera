"""
PriceList domain/model mapper.
"""

from app.domains.price_list.entities.price_list import PriceList
from app.infrastructure.mappers.base_mapper import BaseMapper
from app.models.price_list import PriceList as PriceListModel


class PriceListMapper(BaseMapper[PriceList, PriceListModel]):
    """Maps PriceList between domain and SQLAlchemy model."""

    def to_domain(
        self,
        model: PriceListModel,
    ) -> PriceList:
        """Convert ORM model to domain entity."""

        return PriceList(
            id=model.id,
            name=model.name,
            price_list_type="default",
            description=model.description,
            is_active=model.is_active,
        )

    def to_model(
        self,
        entity: PriceList,
        model: PriceListModel,
    ) -> PriceListModel:
        """Convert domain entity to ORM model."""

        model.name = entity.name
        model.description = entity.description
        model.is_active = entity.is_active

        return model
