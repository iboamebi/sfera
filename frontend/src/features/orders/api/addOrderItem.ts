import type { OrderItemOperation, OrderRead } from "../model/types";
import { http } from "../../../shared/api/http";

interface AddOrderItemRequest {
  instrument_id: string | null;
  instrument_type_id: string | null;
  requested_operations: OrderItemOperation[];
}

export async function addOrderItem(
  orderId: string,
  instrumentId: string | null,
  instrumentTypeId: string | null,
  requestedOperations: OrderItemOperation[],
): Promise<OrderRead> {
  const payload: AddOrderItemRequest = {
    instrument_id: instrumentId,
    instrument_type_id: instrumentTypeId,
    requested_operations: requestedOperations,
  };

  const { data } = await http.post<OrderRead>(
    `/orders/${orderId}/items`,
    payload,
  );

  return data;
}
