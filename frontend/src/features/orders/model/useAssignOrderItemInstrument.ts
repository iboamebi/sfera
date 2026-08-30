import { useMutation, useQueryClient } from "@tanstack/react-query";

import { assignOrderItemInstrument } from "../api/assignOrderItemInstrument";

export function useAssignOrderItemInstrument(orderId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ itemId, instrumentId }: { itemId: string; instrumentId: string }) =>
      assignOrderItemInstrument(orderId, itemId, instrumentId),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["orders", orderId] });
    },
  });
}
