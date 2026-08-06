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
            price_list_type=model.price_list_type,
            currency=model.currency,
            description=model.description,
            valid_from=model.valid_from,
            valid_to=model.valid_to,
            is_active=model.is_active,
            created_at=model.created_at.replace(tzinfo=None),
            updated_at=model.updated_at.replace(tzinfo=None),
        )

    def to_model(
        self,
        entity: PriceList,
        model: PriceListModel,
    ) -> PriceListModel:
        """Convert domain entity to ORM model."""

        model.name = entity.name
        model.price_list_type = entity.price_list_type
        model.currency = entity.currency
        model.description = entity.description
        model.valid_from = entity.valid_from
        model.valid_to = entity.valid_to
        model.is_active = entity.is_active

        return model
