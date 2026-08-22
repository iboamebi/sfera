export interface WarehouseStockRead {
  id: string;
  warehouseId: string;
  warehouseName: string;
  materialId: string;
  materialName: string;
  quantity: number;
  reservedQuantity: number;
  availableQuantity: number;
}
