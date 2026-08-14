import { useMutation, type UseMutationOptions } from "@tanstack/react-query";

import { registerOrder } from "../api/registerOrder";
import type { OrderRead } from "../../model/types";

export function useRegisterOrder(
  options?: UseMutationOptions<OrderRead, Error, string>,
) {
  return useMutation({
    mutationFn: (orderId: string) => registerOrder(orderId),
    ...options,
  });
}
