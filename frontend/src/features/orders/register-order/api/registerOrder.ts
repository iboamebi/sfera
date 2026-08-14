import { http } from "../../../../shared/api/http";
import { mapOrder } from "../../api/orderMapper";
import type { OrderApiDto } from "../../api/types";
import type { OrderRead } from "../../model/types";

export async function registerOrder(
  orderId: string,
): Promise<OrderRead> {
  const response = await http.post<OrderApiDto>(
    `/orders/${orderId}/register`,
  );

  return mapOrder(response.data);
}
