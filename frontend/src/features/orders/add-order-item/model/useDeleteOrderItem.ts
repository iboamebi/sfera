import { useMutation, useQueryClient } from "@tanstack/react-query";

import type { OrderRead } from "../../model/types";
import { deleteOrderItem } from "../api/deleteOrderItem";

export function useDeleteOrderItem(orderId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (itemId: string) => deleteOrderItem(orderId, itemId),
    onSuccess: (order: OrderRead) => {
      queryClient.setQueryData(["orders", orderId], order);
    },
  });
}
