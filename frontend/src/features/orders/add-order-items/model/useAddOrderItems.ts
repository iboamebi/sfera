import { useMutation, useQueryClient } from "@tanstack/react-query";

import type { OrderItemOperation } from "../../model/types";
import { addOrderItems } from "../api/addOrderItems";

export function useAddOrderItems(orderId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      instrumentTypeId,
      quantity,
      requestedOperations,
    }: {
      instrumentTypeId: string;
      quantity: number;
      requestedOperations: OrderItemOperation[];
    }) =>
      addOrderItems(
        orderId,
        instrumentTypeId,
        quantity,
        requestedOperations,
      ),
    onSuccess: async () => {
      await Promise.all([
        queryClient.invalidateQueries({ queryKey: ["orders", orderId] }),
        queryClient.invalidateQueries({ queryKey: ["orders"] }),
      ]);
    },
  });
}
