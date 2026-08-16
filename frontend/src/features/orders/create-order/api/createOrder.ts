import { http } from "../../../../shared/api/http";
import type { OrderRead } from "../../model/types";
import { mapOrder } from "../../api/orderMapper";
import type { OrderApiDto } from "../../api/types";
import type { CreateOrderForm } from "../model/types";

export async function createOrder(data: CreateOrderForm): Promise<OrderRead> {
  const response = await http.post<OrderApiDto>("/orders/", {
    number: data.number,
    customer_id: data.customerId,
    planned_issue_at: data.plannedIssueAt
      ? new Date(data.plannedIssueAt).toISOString()
      : null,
    comment: data.comment?.trim() || null,
  });

  return mapOrder(response.data);
}
