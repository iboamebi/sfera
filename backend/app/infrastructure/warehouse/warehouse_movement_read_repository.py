"""SQLAlchemy read repository for warehouse movement history."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.domains.warehouse.read_models.warehouse_movement_read_models import (
    WarehouseMovementReadData,
)
from app.domains.warehouse.repositories.warehouse_movement_read_repository import (
    WarehouseMovementReadRepository,
)
from app.domains.warehouse.value_objects.movement_type import MovementType
from app.models.material import Material
from app.models.order import Order
from app.models.warehouse import Warehouse
from app.models.warehouse_movement import WarehouseMovement


class WarehouseMovementReadRepositorySQLAlchemy(WarehouseMovementReadRepository):
    """Read-only SQLAlchemy repository for warehouse movements."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def list_by_warehouse(
        self,
        warehouse_id: UUID,
        *,
        material_id: UUID | None,
        order_id: UUID | None,
        movement_type: MovementType | None,
        date_from: datetime | None,
        date_to: datetime | None,
        limit: int,
        offset: int,
    ) -> tuple[list[WarehouseMovementReadData], int]:
        query = (
            self._session.query(
                WarehouseMovement,
                Warehouse.name,
                Material.name,
                Order.number,
            )
            .join(Warehouse, Warehouse.id == WarehouseMovement.warehouse_id)
            .join(Material, Material.id == WarehouseMovement.material_id)
            .outerjoin(Order, Order.id == WarehouseMovement.order_id)
            .filter(
                WarehouseMovement.warehouse_id == warehouse_id,
                WarehouseMovement.archived.is_(False),
            )
        )

        if material_id is not None:
            query = query.filter(WarehouseMovement.material_id == material_id)
        if order_id is not None:
            query = query.filter(WarehouseMovement.order_id == order_id)
        if movement_type is not None:
            query = query.filter(WarehouseMovement.movement_type == movement_type.value)
        if date_from is not None:
            query = query.filter(WarehouseMovement.created_at >= date_from)
        if date_to is not None:
            query = query.filter(WarehouseMovement.created_at <= date_to)

        total = query.with_entities(func.count(WarehouseMovement.id)).scalar() or 0
        rows = (
            query.order_by(
                WarehouseMovement.created_at.desc(),
                WarehouseMovement.id.desc(),
            )
            .offset(offset)
            .limit(limit)
            .all()
        )
        return [
            WarehouseMovementReadData(
                id=movement.id,
                warehouse_id=movement.warehouse_id,
                warehouse_name=warehouse_name,
                material_id=movement.material_id,
                material_name=material_name,
                order_id=movement.order_id,
                order_number=order_number,
                movement_type=MovementType(movement.movement_type.value),
                quantity=float(movement.quantity),
                comment=movement.comment,
                created_at=movement.created_at,
            )
            for movement, warehouse_name, material_name, order_number in rows
        ], total
