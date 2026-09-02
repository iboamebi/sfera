import { useMutation, useQueryClient } from "@tanstack/react-query";

import type { OrderItemOperation, OrderRead } from "../../model/types";
import { addOrderItem } from "../api/addOrderItem";

export function useAddOrderItem(orderId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      instrumentId,
      instrumentTypeId,
      quantity,
      requestedOperations,
    }: {
      instrumentId: string | null;
      instrumentTypeId: string | null;
      quantity: number;
      requestedOperations: OrderItemOperation[];
    }) =>
      addOrderItem(
        orderId,
        instrumentId,
        instrumentTypeId,
        quantity,
        requestedOperations,
      ),
    onSuccess: (order: OrderRead) => {
      queryClient.setQueryData(["orders", orderId], order);
    },
  });
}
