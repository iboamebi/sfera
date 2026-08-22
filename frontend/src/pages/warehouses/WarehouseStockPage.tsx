import { useWarehouseStock } from "../../features/warehouse-stock/queries/useWarehouseStock";
import { WarehouseStockTable } from "../../features/warehouse-stock/ui/WarehouseStockTable";

interface WarehouseStockPageProps {
  warehouseId: string;
}

export function WarehouseStockPage({ warehouseId }: WarehouseStockPageProps) {
  const { data = [], isLoading } = useWarehouseStock(warehouseId);

  if (isLoading) {
    return <div>Загрузка...</div>;
  }

  return <WarehouseStockTable items={data} />;
}
