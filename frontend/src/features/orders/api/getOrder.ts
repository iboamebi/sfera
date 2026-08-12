import { http } from "../../../shared/api/http";
import type { OrderRead } from "../model/types";

export async function getOrder(orderId: string): Promise<OrderRead> {
  const response = await http.get<OrderRead>(`/orders/${orderId}`);

  return response.data;
}
