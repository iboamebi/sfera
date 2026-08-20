"""
Application service for Warehouse.
"""

from uuid import uuid4

from app.application.authorization.authorization import require_role
from app.application.warehouse.commands.add_stock import (
    AddStockCommand,
)
from app.application.warehouse.commands.create_movement import (
    CreateMovementCommand,
)
from app.application.warehouse.commands.create_warehouse import (
    CreateWarehouseCommand,
)
from app.application.warehouse.commands.release_stock import (
    ReleaseStockCommand,
)
from app.application.warehouse.commands.reserve_stock import (
    ReserveStockCommand,
)
from app.application.warehouse.exceptions import (
    StockNotFoundApplicationError,
)
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.domains.warehouse.entities.warehouse import Warehouse
from app.domains.warehouse.entities.warehouse_movement import (
    WarehouseMovement,
)
from app.domains.warehouse.entities.warehouse_stock import (
    WarehouseStock,
)
from app.domains.warehouse.repositories.warehouse_movement_repository import (
    WarehouseMovementRepository,
)
from app.domains.warehouse.repositories.warehouse_repository import (
    WarehouseRepository,
)
from app.domains.warehouse.repositories.warehouse_stock_repository import (
    WarehouseStockRepository,
)
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class WarehouseApplicationService:
    """Coordinates Warehouse use cases."""

    def __init__(
        self,
        warehouse_repository: WarehouseRepository,
        stock_repository: WarehouseStockRepository,
        movement_repository: WarehouseMovementRepository,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._warehouse_repository = warehouse_repository
        self._stock_repository = stock_repository
        self._movement_repository = movement_repository
        self._uow = unit_of_work

    def create(
        self,
        command: CreateWarehouseCommand,
        user: User,
    ) -> Warehouse:
        require_role(
            user,
            UserRole.ADMIN,
            UserRole.WAREHOUSE,
        )

        with self._uow:
            warehouse = Warehouse(
                id=uuid4(),
                name=command.name,
                address=command.address,
                responsible_person=command.responsible_person,
                comment=command.comment,
            )

            self._warehouse_repository.save(warehouse)

        return warehouse

    def add_stock(
        self,
        command: AddStockCommand,
    ) -> WarehouseStock:
        with self._uow:
            stock = WarehouseStock(
                id=uuid4(),
                warehouse_id=command.warehouse_id,
                material_id=command.material_id,
                quantity=command.quantity,
            )

            self._stock_repository.save(stock)

        return stock

    def reserve(
        self,
        command: ReserveStockCommand,
    ) -> WarehouseStock:
        with self._uow:
            stock = self._stock_repository.get_by_material(
                command.warehouse_id,
                command.material_id,
            )

            if stock is None:
                raise StockNotFoundApplicationError

            stock.reserve(command.quantity)

            self._stock_repository.save(stock)

        return stock

    def release(
        self,
        command: ReleaseStockCommand,
    ) -> WarehouseStock:
        with self._uow:
            stock = self._stock_repository.get_by_material(
                command.warehouse_id,
                command.material_id,
            )

            if stock is None:
                raise StockNotFoundApplicationError

            stock.release(command.quantity)

            self._stock_repository.save(stock)

        return stock

    def create_movement(
        self,
        command: CreateMovementCommand,
    ) -> WarehouseMovement:
        with self._uow:
            movement = WarehouseMovement(
                id=uuid4(),
                warehouse_id=command.warehouse_id,
                material_id=command.material_id,
                movement_type=command.movement_type,
                quantity=command.quantity,
                order_id=command.order_id,
                comment=command.comment,
            )

            self._movement_repository.save(movement)

        return movement
