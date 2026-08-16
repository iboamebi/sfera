import { http } from "../../../../shared/api/http";
import type { OrderRead } from "../../model/types";
import { mapOrder } from "../../api/orderMapper";
import type { OrderApiDto } from "../../api/types";

export interface UpdateOrderData {
  plannedIssueAt?: string | null;
  comment?: string | null;
}

export async function updateOrder(
  orderId: string,
  data: UpdateOrderData,
): Promise<OrderRead> {
  const response = await http.patch<OrderApiDto>(
    `/orders/${orderId}`,
    {
      planned_issue_at: data.plannedIssueAt
        ? new Date(data.plannedIssueAt).toISOString()
        : null,
      comment: data.comment?.trim() || null,
    },
  );

  return mapOrder(response.data);
}
