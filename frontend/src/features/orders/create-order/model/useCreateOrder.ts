import { useMutation, type UseMutationOptions } from "@tanstack/react-query";

import { createOrder } from "../api/createOrder";
import type { OrderRead } from "../../model/types";
import type { CreateOrderForm } from "./types";

export function useCreateOrder(
  options?: UseMutationOptions<OrderRead, Error, CreateOrderForm>,
) {
  return useMutation({
    mutationFn: (data: CreateOrderForm) => createOrder(data),
    ...options,
  });
}
