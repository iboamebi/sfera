"""
Warehouse mapper.
"""

from app.domains.warehouse.entities.warehouse import Warehouse
from app.infrastructure.mappers.base_mapper import BaseMapper
from app.models.warehouse import Warehouse as WarehouseModel


class WarehouseMapper(
    BaseMapper[
        Warehouse,
        WarehouseModel,
    ],
):
    """Map warehouse between domain and ORM."""

    def to_domain(
        self,
        model: WarehouseModel,
    ) -> Warehouse:
        """Convert ORM model to domain entity."""

        return Warehouse(
            id=model.id,
            name=model.name,
            address=model.address,
            responsible_person=model.responsible_person,
            comment=model.comment,
            archived=model.archived,
        )

    def to_model(
        self,
        entity: Warehouse,
        model: WarehouseModel,
    ) -> WarehouseModel:
        """Convert domain entity to ORM model."""

        model.name = entity.name
        model.address = entity.address
        model.responsible_person = entity.responsible_person
        model.comment = entity.comment
        model.archived = entity.archived

        return model
