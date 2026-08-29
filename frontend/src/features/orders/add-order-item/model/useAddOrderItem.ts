import { useMutation, useQueryClient } from "@tanstack/react-query";

import type { OrderItemOperation, OrderRead } from "../../model/types";
import { addOrderItem } from "../api/addOrderItem";

export function useAddOrderItem(orderId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      instrumentId,
      requestedOperations,
    }: {
      instrumentId: string | null;
      requestedOperations: OrderItemOperation[];
    }) => addOrderItem(orderId, instrumentId, requestedOperations),
    onSuccess: (order: OrderRead) => {
      queryClient.setQueryData(["orders", orderId], order);
    },
  });
}
