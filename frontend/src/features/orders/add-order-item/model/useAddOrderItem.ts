import { useMutation, useQueryClient } from "@tanstack/react-query";

import type { OrderRead } from "../../model/types";
import { addOrderItem } from "../api/addOrderItem";

export function useAddOrderItem(orderId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (instrumentId: string | null) =>
      addOrderItem(orderId, instrumentId),
    onSuccess: async (_order: OrderRead) => {
      await queryClient.invalidateQueries({ queryKey: ["orders", orderId] });
    },
  });
}
