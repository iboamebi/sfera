import { http } from "../../../shared/api/http";

export async function assignOrderItemInstrument(
  orderId: string,
  itemId: string,
  instrumentId: string,
): Promise<void> {
  await http.patch(`/orders/${orderId}/items/${itemId}/instrument`, {
    instrument_id: instrumentId,
  });
}
