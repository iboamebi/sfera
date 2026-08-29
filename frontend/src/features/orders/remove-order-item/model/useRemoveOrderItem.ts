import { useMutation, useQueryClient } from "@tanstack/react-query";

import type { OrderRead } from "../../model/types";
import { removeOrderItem } from "../api/removeOrderItem";

export function useRemoveOrderItem(orderId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (itemId: string) => removeOrderItem(orderId, itemId),
    onSuccess: (order: OrderRead) => {
      queryClient.setQueryData(["orders", orderId], order);
    },
  });
}
