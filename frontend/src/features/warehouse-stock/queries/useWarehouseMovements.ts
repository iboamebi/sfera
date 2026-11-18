import { useQuery } from "@tanstack/react-query";

import {
  getWarehouseMovements,
  type WarehouseMovementFilters,
} from "../api/warehouseMovementApi";
import { mapWarehouseMovement } from "../model/movementTypes";

export const warehouseMovementKeys = {
  all: ["warehouse-movements"] as const,
  byWarehouse: (warehouseId: string, filters: WarehouseMovementFilters) =>
    [...warehouseMovementKeys.all, warehouseId, filters] as const,
};

export function useWarehouseMovements(
  warehouseId: string,
  filters: WarehouseMovementFilters,
) {
  return useQuery({
    queryKey: warehouseMovementKeys.byWarehouse(warehouseId, filters),
    queryFn: async () => {
      const page = await getWarehouseMovements(warehouseId, filters);
      return {
        ...page,
        items: page.items.map(mapWarehouseMovement),
      };
    },
    enabled: Boolean(warehouseId),
  });
}
