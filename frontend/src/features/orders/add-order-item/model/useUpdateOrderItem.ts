import { useMutation, useQueryClient } from "@tanstack/react-query";

import type { OrderItemOperation, OrderRead } from "../../model/types";
import { updateOrderItem } from "../api/updateOrderItem";

export function useUpdateOrderItem(orderId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      itemId,
      requestedOperations,
    }: {
      itemId: string;
      requestedOperations: OrderItemOperation[];
    }) => updateOrderItem(orderId, itemId, requestedOperations),
    onSuccess: (order: OrderRead) => {
      queryClient.setQueryData(["orders", orderId], order);
    },
  });
}
