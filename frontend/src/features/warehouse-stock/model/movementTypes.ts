import type {
  WarehouseMovementApiDto,
  WarehouseMovementType,
} from "../api/warehouseMovementApi";

export interface WarehouseMovementRead {
  id: string;
  materialId: string;
  materialName: string;
  orderId: string | null;
  orderNumber: string | null;
  movementType: WarehouseMovementType;
  quantity: number;
  comment: string | null;
  createdAt: string;
}

export function mapWarehouseMovement(
  dto: WarehouseMovementApiDto,
): WarehouseMovementRead {
  return {
    id: dto.id,
    materialId: dto.material_id,
    materialName: dto.material_name,
    orderId: dto.order_id,
    orderNumber: dto.order_number,
    movementType: dto.movement_type,
    quantity: dto.quantity,
    comment: dto.comment,
    createdAt: dto.created_at,
  };
}
