import { http } from "../../../shared/api/http";
import { mapOrder } from "./orderMapper";
import type { OrderRead } from "../model/types";
import type { OrderApiDto } from "./types";

export async function getOrders(): Promise<OrderRead[]> {
  const response = await http.get<OrderApiDto[]>("/orders/");

  return response.data.map(mapOrder);
}
