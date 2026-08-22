import { useQuery } from "@tanstack/react-query";

import { getWarehouseStocks } from "../api/warehouseStockApi";
import { mapWarehouseStock } from "../model/mapper";

export const warehouseStockKeys = {
  all: ["warehouse-stocks"] as const,
  byWarehouse: (warehouseId: string) =>
    [...warehouseStockKeys.all, warehouseId] as const,
};

export function useWarehouseStock(warehouseId: string) {
  return useQuery({
    queryKey: warehouseStockKeys.byWarehouse(warehouseId),
    queryFn: async () => {
      const items = await getWarehouseStocks(warehouseId);
      return items.map(mapWarehouseStock);
    },
    enabled: Boolean(warehouseId),
  });
}
