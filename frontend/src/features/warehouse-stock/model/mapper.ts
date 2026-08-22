import type { WarehouseStockRead } from "./types";

export interface WarehouseStockApiDto {
  id: string;
  warehouse_id: string;
  warehouse_name: string;
  material_id: string;
  material_name: string;
  quantity: number;
  reserved_quantity: number;
  available_quantity: number;
}

export function mapWarehouseStock(
  dto: WarehouseStockApiDto,
): WarehouseStockRead {
  return {
    id: dto.id,
    warehouseId: dto.warehouse_id,
    warehouseName: dto.warehouse_name,
    materialId: dto.material_id,
    materialName: dto.material_name,
    quantity: dto.quantity,
    reservedQuantity: dto.reserved_quantity,
    availableQuantity: dto.available_quantity,
  };
}
