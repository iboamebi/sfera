import { useMutation, useQueryClient } from "@tanstack/react-query";

import { deleteOrderItem } from "../api/deleteOrderItem";

export function useDeleteOrderItem(orderId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (itemId: string) => deleteOrderItem(orderId, itemId),
    onSuccess: async () => {
      await Promise.all([
        queryClient.invalidateQueries({ queryKey: ["orders", orderId] }),
        queryClient.invalidateQueries({ queryKey: ["orders"] }),
      ]);
    },
  });
}
