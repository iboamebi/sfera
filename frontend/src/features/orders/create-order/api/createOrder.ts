import type { CreateOrderForm } from "../model/types";

export interface OrderRead {
  id: string;
  number: string;
  customer_id: string;
}

export async function createOrder(
  data: CreateOrderForm,
): Promise<OrderRead> {
  const response = await fetch("/orders/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      number: data.number,
      customer_id: data.customerId,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to create order");
  }

  return response.json() as Promise<OrderRead>;
}
