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
from app.models.warehouse_movement import (
    WarehouseMovement as WarehouseMovementModel,
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
        self._mapper = WarehouseMovementMapper()

    def save(
        self,
        movement: WarehouseMovement,
    ) -> None:
        """Save warehouse movement."""

        model = self._session.get(
            WarehouseMovementModel,
            movement.id,
        )

        if model is None:
            model = WarehouseMovementModel(
                id=movement.id,
            )
            self._session.add(model)

        self._mapper.to_model(
            movement,
            model,
        )

        self._session.flush()
