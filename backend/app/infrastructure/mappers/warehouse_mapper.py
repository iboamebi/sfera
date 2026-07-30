"""
Warehouse mapper.
"""

from app.domains.warehouse.entities.warehouse import Warehouse
from app.models.warehouse import Warehouse as WarehouseModel


class WarehouseMapper:
    """Map warehouse between domain and ORM."""

    @staticmethod
    def to_domain(
        model: WarehouseModel,
    ) -> Warehouse:
        return Warehouse(
            id=model.id,
            name=model.name,
            address=model.address,
            responsible_person=model.responsible_person,
            comment=model.comment,
            archived=model.archived,
        )

    @staticmethod
    def to_model(
        entity: Warehouse,
    ) -> WarehouseModel:
        return WarehouseModel(
            id=entity.id,
            name=entity.name,
            address=entity.address,
            responsible_person=entity.responsible_person,
            comment=entity.comment,
            archived=entity.archived,
        )
