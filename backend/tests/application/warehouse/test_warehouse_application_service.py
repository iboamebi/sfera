from uuid import UUID, uuid4

import pytest

from app.application.authorization.authorization import AuthorizationError
from app.application.warehouse.commands.add_stock import AddStockCommand
from app.application.warehouse.commands.create_movement import CreateMovementCommand
from app.application.warehouse.exceptions import (
    UnsupportedWarehouseMovementApplicationError,
)
from app.application.warehouse.services.warehouse_application_service import (
    WarehouseApplicationService,
)
from app.domains.user.entities.user import User
from app.domains.user.value_objects.user_role import UserRole
from app.domains.warehouse.entities.warehouse_stock import WarehouseStock
from app.domains.warehouse.value_objects.movement_type import MovementType
from app.shared.unit_of_work.unit_of_work import UnitOfWork


class FakeUnitOfWork(UnitOfWork):
    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass

    def register_aggregate(
        self, aggregate: object, operation_id: UUID | None = None
    ) -> None:
        pass


class FakeStockRepository:
    def __init__(self) -> None:
        self.items: dict[tuple[UUID, UUID], WarehouseStock] = {}

    def get_by_material(
        self, warehouse_id: UUID, material_id: UUID
    ) -> WarehouseStock | None:
        return self.items.get((warehouse_id, material_id))

    def save(self, stock: WarehouseStock) -> None:
        self.items[(stock.warehouse_id, stock.material_id)] = stock


class FakeMovementRepository:
    def __init__(self) -> None:
        self.items = []

    def save(self, movement) -> None:
        self.items.append(movement)


def make_user(role: UserRole = UserRole.WAREHOUSE) -> User:
    return User(
        id=uuid4(),
        username="warehouse-test",
        password_hash="test-hash",
        role=role,
    )


def make_service():
    stocks = FakeStockRepository()
    movements = FakeMovementRepository()
    service = WarehouseApplicationService(
        object(),
        stocks,
        movements,
        FakeUnitOfWork(),
    )
    return service, stocks, movements


def test_receipt_updates_existing_stock_and_records_movement() -> None:
    service, stocks, movements = make_service()
    warehouse_id = uuid4()
    material_id = uuid4()
    user = make_user()

    first = service.add_stock(
        AddStockCommand(warehouse_id, material_id, 10),
        user,
    )
    second = service.add_stock(
        AddStockCommand(warehouse_id, material_id, 5),
        user,
    )

    assert first.id == second.id
    assert second.quantity == 15
    assert len(stocks.items) == 1
    assert [movement.movement_type for movement in movements.items] == [
        MovementType.RECEIPT,
        MovementType.RECEIPT,
    ]
    assert [movement.quantity for movement in movements.items] == [10, 5]


def test_issue_reduces_stock_and_records_movement() -> None:
    service, stocks, movements = make_service()
    warehouse_id = uuid4()
    material_id = uuid4()
    stock = WarehouseStock(
        id=uuid4(),
        warehouse_id=warehouse_id,
        material_id=material_id,
        quantity=12,
    )
    stocks.save(stock)

    service.create_movement(
        CreateMovementCommand(
            warehouse_id, material_id, MovementType.ISSUE, 4
        ),
        make_user(),
    )

    assert stock.quantity == 8
    assert movements.items[0].movement_type == MovementType.ISSUE


def test_issue_cannot_reduce_stock_below_reserved_quantity() -> None:
    service, stocks, movements = make_service()
    warehouse_id = uuid4()
    material_id = uuid4()
    stock = WarehouseStock(
        id=uuid4(),
        warehouse_id=warehouse_id,
        material_id=material_id,
        quantity=10,
        reserved_quantity=7,
    )
    stocks.save(stock)

    with pytest.raises(Exception):
        service.create_movement(
            CreateMovementCommand(
                warehouse_id, material_id, MovementType.ISSUE, 4
            ),
            make_user(),
        )

    assert stock.quantity == 10
    assert movements.items == []


def test_adjustment_is_rejected_until_its_direction_is_defined() -> None:
    service, _, movements = make_service()

    with pytest.raises(UnsupportedWarehouseMovementApplicationError):
        service.create_movement(
            CreateMovementCommand(
                uuid4(), uuid4(), MovementType.ADJUSTMENT, 1
            ),
            make_user(),
        )

    assert movements.items == []


def test_stock_write_rejects_unauthorized_user() -> None:
    service, stocks, movements = make_service()

    with pytest.raises(AuthorizationError):
        service.add_stock(
            AddStockCommand(uuid4(), uuid4(), 1),
            make_user(UserRole.OPERATOR),
        )

    assert stocks.items == {}
    assert movements.items == []
