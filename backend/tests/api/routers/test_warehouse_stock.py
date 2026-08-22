from uuid import uuid4

from app.api.routers.warehouse_stock import get_warehouse_stock
from app.domains.warehouse.read_models.warehouse_stock_read_models import (
    WarehouseStockReadData,
)


def test_get_warehouse_stock_returns_read_contract() -> None:
    warehouse_id = uuid4()

    class FakeWarehouseStockReadService:
        def get_by_warehouse(
            self,
            requested_id: object,
        ) -> list[WarehouseStockReadData]:
            assert requested_id == warehouse_id

            return [
                WarehouseStockReadData(
                    id=uuid4(),
                    warehouse_id=warehouse_id,
                    warehouse_name="Main warehouse",
                    material_id=uuid4(),
                    material_name="Material A",
                    quantity=100,
                    reserved_quantity=20,
                    available_quantity=80,
                ),
            ]

    result = get_warehouse_stock(
        warehouse_id=warehouse_id,
        service=FakeWarehouseStockReadService(),
    )

    assert len(result) == 1
    assert result[0].warehouse_id == warehouse_id
    assert result[0].material_name == "Material A"
    assert result[0].available_quantity == 80
