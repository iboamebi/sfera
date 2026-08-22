import { useParams } from "react-router";

import { useWarehouseStock } from "../../features/warehouse-stock/queries/useWarehouseStock";
import { WarehouseStockTable } from "../../features/warehouse-stock/ui/WarehouseStockTable";

export function WarehouseStockPage() {
  const { warehouseId } = useParams<{ warehouseId: string }>();

  if (!warehouseId) {
    return null;
  }

  const { data, isLoading } = useWarehouseStock(warehouseId);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return <WarehouseStockTable items={data ?? []} />;
}
