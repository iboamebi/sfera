import { useMutation, useQueryClient } from "@tanstack/react-query";

import type { OrderRead } from "../../model/types";
import { assignOrderItemInstrument } from "../api/assignOrderItemInstrument";

/** Assigns a concrete instrument to an existing order item. */
export function useAssignOrderItemInstrument(orderId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      itemId,
      instrumentId,
    }: {
      itemId: string;
      instrumentId: string;
    }) => assignOrderItemInstrument(orderId, itemId, instrumentId),
    onSuccess: (order: OrderRead) => {
      queryClient.setQueryData(["orders", orderId], order);
    },
  });
}
