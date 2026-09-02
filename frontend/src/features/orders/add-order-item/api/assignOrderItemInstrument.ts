import { http } from "../../../../shared/api/http";
import { mapOrder } from "../../api/orderMapper";
import type { OrderApiDto } from "../../api/types";
import type { OrderRead } from "../../model/types";

/** Assigns a concrete instrument to an existing order item. */
export async function assignOrderItemInstrument(
  orderId: string,
  itemId: string,
  instrumentId: string,
): Promise<OrderRead> {
  const response = await http.patch<OrderApiDto>(
    `/orders/${orderId}/items/${itemId}/instrument`,
    { instrument_id: instrumentId },
  );

  return mapOrder(response.data);
}
