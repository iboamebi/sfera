import { useMutation, useQueryClient } from "@tanstack/react-query";

import { removeOrderItem } from "../api/removeOrderItem";

export function useRemoveOrderItem(orderId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (itemId: string) => removeOrderItem(orderId, itemId),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["orders", orderId] });
    },
  });
}
