import { http } from "../../../../shared/api/http";
import { mapOrder } from "../../api/orderMapper";
import type { OrderApiDto } from "../../api/types";
import type { OrderRead } from "../../model/types";

interface AddOrderItemRequest {
  instrument_id: string | null;
}

export async function addOrderItem(
  orderId: string,
  instrumentId: string | null,
): Promise<OrderRead> {
  const response = await http.post<OrderApiDto>(
    `/orders/${orderId}/items`,
    {
      instrument_id: instrumentId,
    } satisfies AddOrderItemRequest,
  );

  return mapOrder(response.data);
}
