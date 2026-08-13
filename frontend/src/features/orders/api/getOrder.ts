import { http } from "../../../shared/api/http";
import { mapOrder } from "./orderMapper";
import type { OrderApiDto } from "./types";
import type { OrderRead } from "../model/types";

export async function getOrder(orderId: string): Promise<OrderRead> {
  const response = await http.get<OrderApiDto>(`/orders/${orderId}`);

  return mapOrder(response.data);
}
