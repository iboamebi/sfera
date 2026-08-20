import { useMutation, useQueryClient } from "@tanstack/react-query";

import { addOrderItem } from "../api/addOrderItem";
import type { OrderRead } from "../../model/types";

export function useAddOrderItem(orderId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (instrumentId: string | null) =>
      addOrderItem(orderId, instrumentId),
    onSuccess: (order: OrderRead) => {
      queryClient.setQueryData(["orders", orderId], order);
    },
  });
}
