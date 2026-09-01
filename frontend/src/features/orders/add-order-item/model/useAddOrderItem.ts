import { useMutation, useQueryClient } from "@tanstack/react-query";

import type { OrderItemOperation, OrderRead } from "../../model/types";
import { addOrderItem } from "../api/addOrderItem";

export function useAddOrderItem(orderId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      instrumentId,
      instrumentTypeId,
      requestedOperations,
    }: {
      instrumentId: string | null;
      instrumentTypeId: string | null;
      requestedOperations: OrderItemOperation[];
    }) =>
      addOrderItem(
        orderId,
        instrumentId,
        instrumentTypeId,
        requestedOperations,
      ),
    onSuccess: (order: OrderRead) => {
      queryClient.setQueryData(["orders", orderId], order);
    },
  });
}
