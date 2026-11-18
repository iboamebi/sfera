"""
Application service for Warehouse.
"""

from uuid import uuid4

from app.application.authorization.authorization import require_role
from app.application.warehouse.commands.add_stock import AddStockCommand
from app.application.warehouse.commands.create_movement import CreateMovementCommand
from app.application.warehouse.commands.create_warehouse import CreateWarehouseCommand
from app.application.warehouse.commands.release_stock import ReleaseStockCommand
from app.application.warehouse.commands.reserve_stock import ReserveStockCommand
from app.application.warehouse.exceptions import (
    StockNotFoundApplicationError,
    UnsupportedWarehouseMovementApplicationError,
)
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.domains.warehouse.entities.warehouse import Warehouse
from app.domains.warehouse.entities.warehouse_movement import WarehouseMovement
from app.domains.warehouse.entities.warehouse_stock import WarehouseStock
from app.domains.warehouse.repositories.warehouse_movement_repository import (
    WarehouseMovementRepository,
)
from app.domains.warehouse.repositories.warehouse_repository import WarehouseRepository
from app.domains.warehouse.repositories.warehouse_stock_repository import (
    WarehouseStockRepository,
)
from app.domains.warehouse.value_objects.movement_type import MovementType
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

    def create(self, command: CreateWarehouseCommand, user: User) -> Warehouse:
        """Create warehouse."""
        require_role(user, UserRole.ADMIN, UserRole.WAREHOUSE)

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

    def _get_or_create_stock(self, warehouse_id, material_id) -> WarehouseStock:
        stock = self._stock_repository.get_by_material(warehouse_id, material_id)
        if stock is None:
            stock = WarehouseStock(
                id=uuid4(),
                warehouse_id=warehouse_id,
                material_id=material_id,
            )
        return stock

    def _save_movement(
        self,
        warehouse_id,
        material_id,
        movement_type: MovementType,
        quantity: float,
        order_id=None,
        comment=None,
    ) -> WarehouseMovement:
        movement = WarehouseMovement(
            id=uuid4(),
            warehouse_id=warehouse_id,
            material_id=material_id,
            movement_type=movement_type,
            quantity=quantity,
            order_id=order_id,
            comment=comment,
        )
        self._movement_repository.save(movement)
        return movement

    def add_stock(self, command: AddStockCommand, user: User) -> WarehouseStock:
        """Register stock receipt and update balance atomically."""
        require_role(user, UserRole.ADMIN, UserRole.WAREHOUSE)

        with self._uow:
            stock = self._get_or_create_stock(command.warehouse_id, command.material_id)
            stock.add(command.quantity)
            self._stock_repository.save(stock)
            self._save_movement(
                command.warehouse_id,
                command.material_id,
                MovementType.RECEIPT,
                command.quantity,
            )

        return stock

    def reserve(self, command: ReserveStockCommand, user: User) -> WarehouseStock:
        """Reserve available stock and record the reservation atomically."""
        require_role(user, UserRole.ADMIN, UserRole.WAREHOUSE)

        with self._uow:
            stock = self._stock_repository.get_by_material(
                command.warehouse_id, command.material_id
            )
            if stock is None:
                raise StockNotFoundApplicationError

            stock.reserve(command.quantity)
            self._stock_repository.save(stock)
            self._save_movement(
                command.warehouse_id,
                command.material_id,
                MovementType.RESERVATION,
                command.quantity,
                command.order_id,
            )

        return stock

    def release(self, command: ReleaseStockCommand, user: User) -> WarehouseStock:
        """Release reserved stock and record the release atomically."""
        require_role(user, UserRole.ADMIN, UserRole.WAREHOUSE)

        with self._uow:
            stock = self._stock_repository.get_by_material(
                command.warehouse_id, command.material_id
            )
            if stock is None:
                raise StockNotFoundApplicationError

            stock.release(command.quantity)
            self._stock_repository.save(stock)
            self._save_movement(
                command.warehouse_id,
                command.material_id,
                MovementType.RELEASE,
                command.quantity,
                command.order_id,
            )

        return stock

    def create_movement(
        self, command: CreateMovementCommand, user: User
    ) -> WarehouseMovement:
        """Apply a stock operation and append its immutable movement record."""
        require_role(user, UserRole.ADMIN, UserRole.WAREHOUSE)

        if command.movement_type == MovementType.ADJUSTMENT:
            raise UnsupportedWarehouseMovementApplicationError

        with self._uow:
            if command.movement_type == MovementType.RECEIPT:
                stock = self._get_or_create_stock(
                    command.warehouse_id, command.material_id
                )
                stock.add(command.quantity)
            else:
                stock = self._stock_repository.get_by_material(
                    command.warehouse_id, command.material_id
                )
                if stock is None:
                    raise StockNotFoundApplicationError

                if command.movement_type == MovementType.ISSUE:
                    stock.remove(command.quantity)
                elif command.movement_type == MovementType.RESERVATION:
                    stock.reserve(command.quantity)
                elif command.movement_type == MovementType.RELEASE:
                    stock.release(command.quantity)
                else:
                    raise UnsupportedWarehouseMovementApplicationError

            self._stock_repository.save(stock)
            movement = self._save_movement(
                command.warehouse_id,
                command.material_id,
                command.movement_type,
                command.quantity,
                command.order_id,
                command.comment,
            )

        return movement
