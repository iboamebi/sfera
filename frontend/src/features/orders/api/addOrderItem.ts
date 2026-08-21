import { http } from "../../../shared/api/http";

interface AddOrderItemRequest {
  instrument_id: string;
}

export async function addOrderItem(
  orderId: string,
  instrumentId: string,
): Promise<void> {
  const payload: AddOrderItemRequest = {
    instrument_id: instrumentId,
  };

  await http.post(`/orders/${orderId}/items`, payload);
}
