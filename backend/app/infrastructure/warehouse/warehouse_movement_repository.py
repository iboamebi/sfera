"""
SQLAlchemy warehouse movement repository.
"""

from sqlalchemy.orm import Session

from app.domains.warehouse.entities.warehouse_movement import (
    WarehouseMovement,
)
from app.domains.warehouse.repositories.warehouse_movement_repository import (
    WarehouseMovementRepository,
)
from app.infrastructure.mappers.warehouse_movement_mapper import (
    WarehouseMovementMapper,
)


class WarehouseMovementRepositorySQLAlchemy(
    WarehouseMovementRepository,
):
    """SQLAlchemy warehouse movement repository."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def save(
        self,
        movement: WarehouseMovement,
    ) -> None:
        model = WarehouseMovementMapper.to_model(
            movement,
        )

        self._session.merge(
            model,
        )
