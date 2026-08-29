import { http } from "../../../../shared/api/http";
import { mapOrder } from "../../api/orderMapper";
import type { OrderApiDto } from "../../api/types";
import type { OrderItemOperation, OrderRead } from "../../model/types";

interface AddOrderItemsRequest {
  instrument_type_id: string;
  quantity: number;
  requested_operations: OrderItemOperation[];
}

export async function addOrderItems(
  orderId: string,
  instrumentTypeId: string,
  quantity: number,
  requestedOperations: OrderItemOperation[],
): Promise<OrderRead> {
  const response = await http.post<OrderApiDto>(
    `/orders/${orderId}/items/bulk`,
    {
      instrument_type_id: instrumentTypeId,
      quantity,
      requested_operations: requestedOperations,
    } satisfies AddOrderItemsRequest,
  );

  return mapOrder(response.data);
}
