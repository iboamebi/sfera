import axios from "axios";

export type WarehouseMovementType =
  | "RECEIPT"
  | "ISSUE"
  | "RESERVATION"
  | "RELEASE"
  | "ADJUSTMENT";

export interface WarehouseMovementApiDto {
  id: string;
  warehouse_id: string;
  warehouse_name: string;
  material_id: string;
  material_name: string;
  order_id: string | null;
  order_number: string | null;
  movement_type: WarehouseMovementType;
  quantity: number;
  comment: string | null;
  created_at: string;
}

export interface WarehouseMovementPageApiDto {
  items: WarehouseMovementApiDto[];
  total: number;
  limit: number;
  offset: number;
}

export interface WarehouseMovementFilters {
  materialId?: string;
  orderId?: string;
  movementType?: WarehouseMovementType;
  dateFrom?: string;
  dateTo?: string;
  limit?: number;
  offset?: number;
}

export async function getWarehouseMovements(
  warehouseId: string,
  filters: WarehouseMovementFilters,
): Promise<WarehouseMovementPageApiDto> {
  const response = await axios.get<WarehouseMovementPageApiDto>(
    `/warehouse-movements/warehouse/${warehouseId}`,
    {
      params: {
        material_id: filters.materialId || undefined,
        order_id: filters.orderId || undefined,
        movement_type: filters.movementType || undefined,
        date_from: filters.dateFrom || undefined,
        date_to: filters.dateTo || undefined,
        limit: filters.limit ?? 50,
        offset: filters.offset ?? 0,
      },
    },
  );

  return response.data;
}
