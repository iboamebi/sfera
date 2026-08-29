import { http } from "../../../../shared/api/http";

export async function deleteOrderItem(
  orderId: string,
  itemId: string,
): Promise<void> {
  await http.delete(`/orders/${orderId}/items/${itemId}`);
}
