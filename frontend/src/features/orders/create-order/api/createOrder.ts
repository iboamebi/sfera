import { http } from "../../../../shared/api/http";
import type { CreateOrderForm } from "../model/types";

export interface OrderRead {
  id: string;
  number: string;
  customer_id: string;
}

export async function createOrder(
  data: CreateOrderForm,
): Promise<OrderRead> {
  const response = await http.post<OrderRead>("/orders/", {
    number: data.number,
    customer_id: data.customerId,
  });

  return response.data;
}
