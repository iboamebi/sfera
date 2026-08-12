import { useMutation } from "@tanstack/react-query";

import { createOrder } from "../api/createOrder";
import type { CreateOrderForm } from "./types";

export function useCreateOrder() {
  return useMutation({
    mutationFn: (data: CreateOrderForm) => createOrder(data),
  });
}
