from datetime import UTC, datetime
from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.api.routers.warehouse_movement import list_warehouse_movements
from app.domains.warehouse.read_models.warehouse_movement_read_models import (
    WarehouseMovementReadData,
)
from app.domains.warehouse.value_objects.movement_type import MovementType


def test_list_warehouse_movements_returns_page_and_forwards_filters() -> None:
    warehouse_id = uuid4()
    material_id = uuid4()
    order_id = uuid4()
    date_from = datetime(2026, 1, 1, tzinfo=UTC)
    date_to = datetime(2026, 12, 31, tzinfo=UTC)

    class FakeWarehouseMovementReadService:
        def list_by_warehouse(self, requested_id, **filters):
            assert requested_id == warehouse_id
            assert filters == {
                "material_id": material_id,
                "order_id": order_id,
                "movement_type": MovementType.ISSUE,
                "date_from": date_from,
                "date_to": date_to,
                "limit": 25,
                "offset": 10,
            }
            return [
                WarehouseMovementReadData(
                    id=uuid4(),
                    warehouse_id=warehouse_id,
                    warehouse_name="Main warehouse",
                    material_id=material_id,
                    material_name="Material A",
                    order_id=order_id,
                    order_number="10025",
                    movement_type=MovementType.ISSUE,
                    quantity=2.5,
                    comment="Used for repair",
                    created_at=datetime(2026, 6, 1, tzinfo=UTC),
                )
            ], 31

    result = list_warehouse_movements(
        warehouse_id=warehouse_id,
        material_id=material_id,
        order_id=order_id,
        movement_type=MovementType.ISSUE,
        date_from=date_from,
        date_to=date_to,
        limit=25,
        offset=10,
        service=FakeWarehouseMovementReadService(),
    )

    assert result.total == 31
    assert result.limit == 25
    assert result.offset == 10
    assert result.items[0].order_number == "10025"
    assert result.items[0].quantity == 2.5


def test_list_warehouse_movements_rejects_reversed_date_range() -> None:
    class FakeWarehouseMovementReadService:
        def list_by_warehouse(self, requested_id, **filters):
            pytest.fail("Service must not be called for an invalid date range")

    with pytest.raises(HTTPException) as error:
        list_warehouse_movements(
            warehouse_id=uuid4(),
            date_from=datetime(2026, 12, 31, tzinfo=UTC),
            date_to=datetime(2026, 1, 1, tzinfo=UTC),
            service=FakeWarehouseMovementReadService(),
        )

    assert error.value.status_code == 422
