import { http } from "../../../../shared/api/http";
import { mapOrder } from "../../api/orderMapper";
import type { OrderApiDto } from "../../api/types";
import type { OrderItemOperation, OrderRead } from "../../model/types";

export async function updateOrderItem(
  orderId: string,
  itemId: string,
  requestedOperations: OrderItemOperation[],
): Promise<OrderRead> {
  const response = await http.patch<OrderApiDto>(
    `/orders/${orderId}/items/${itemId}`,
    { requested_operations: requestedOperations },
  );

  return mapOrder(response.data);
}
