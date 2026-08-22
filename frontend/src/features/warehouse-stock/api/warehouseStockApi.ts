import axios from "axios";

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

export async function getWarehouseStocks(
  warehouseId: string,
): Promise<WarehouseStockApiDto[]> {
  const response = await axios.get<WarehouseStockApiDto[]>(
    `/warehouse-stocks/warehouse/${warehouseId}`,
  );

  return response.data;
}
