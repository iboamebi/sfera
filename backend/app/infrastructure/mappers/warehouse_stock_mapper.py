"""
Warehouse stock mapper.
"""

from app.domains.warehouse.entities.warehouse_stock import (
    WarehouseStock,
)
from app.models.warehouse_stock import (
    WarehouseStock as WarehouseStockModel,
)


class WarehouseStockMapper:
    """Map warehouse stock between domain and ORM."""

    @staticmethod
    def to_domain(
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

    @staticmethod
    def to_model(
        entity: WarehouseStock,
    ) -> WarehouseStockModel:
        return WarehouseStockModel(
            id=entity.id,
            warehouse_id=entity.warehouse_id,
            material_id=entity.material_id,
            quantity=entity.quantity,
            reserved_quantity=entity.reserved_quantity,
            archived=entity.archived,
        )
