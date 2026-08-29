import { http } from "../../../../shared/api/http";
import { mapOrder } from "../../api/orderMapper";
import type { OrderApiDto } from "../../api/types";
import type { OrderItemOperation, OrderRead } from "../../model/types";

interface AddOrderItemRequest {
  instrument_id: string | null;
  requested_operations: OrderItemOperation[];
}

export async function addOrderItem(
  orderId: string,
  instrumentId: string | null,
  requestedOperations: OrderItemOperation[],
): Promise<OrderRead> {
  const response = await http.post<OrderApiDto>(
    `/orders/${orderId}/items`,
    {
      instrument_id: instrumentId,
      requested_operations: requestedOperations,
    } satisfies AddOrderItemRequest,
  );

  return mapOrder(response.data);
}
