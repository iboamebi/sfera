import { http } from "../../../../shared/api/http";
import { mapOrder } from "../../api/orderMapper";
import type { OrderApiDto } from "../../api/types";
import type { OrderRead } from "../../model/types";

export async function removeOrderItem(
  orderId: string,
  itemId: string,
): Promise<OrderRead> {
  const response = await http.delete<OrderApiDto>(
    `/orders/${orderId}/items/${itemId}`,
  );

  return mapOrder(response.data);
}
