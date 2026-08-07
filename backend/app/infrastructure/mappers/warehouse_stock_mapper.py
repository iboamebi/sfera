"""
Warehouse stock mapper.
"""

from app.domains.warehouse.entities.warehouse_stock import WarehouseStock
from app.infrastructure.mappers.base_mapper import BaseMapper
from app.models.warehouse_stock import (
    WarehouseStock as WarehouseStockModel,
)


class WarehouseStockMapper(
    BaseMapper[
        WarehouseStock,
        WarehouseStockModel,
    ],
):
    """Map warehouse stock between domain and ORM."""

    def to_domain(
        self,
        model: WarehouseStockModel,
    ) -> WarehouseStock:
        return WarehouseStock(
            id=model.id,
            warehouse_id=model.warehouse_id,
            material_id=model.material_id,
            quantity=float(model.quantity),
            reserved_quantity=float(model.reserved_quantity),
            archived=model.archived,
        )

    def to_model(
        self,
        entity: WarehouseStock,
        model: WarehouseStockModel,
    ) -> WarehouseStockModel:
        model.warehouse_id = entity.warehouse_id
        model.material_id = entity.material_id
        model.quantity = entity.quantity
        model.reserved_quantity = entity.reserved_quantity
        model.archived = entity.archived

        return model
