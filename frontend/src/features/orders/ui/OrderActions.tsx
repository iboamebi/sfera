import { Alert, Stack } from "@mui/material";
import { useQueryClient } from "@tanstack/react-query";

import type { OrderRead } from "../model/types";
import { useRegisterOrder } from "../register-order/model/useRegisterOrder";
import { RegisterOrderButton } from "../register-order/ui/RegisterOrderButton";
import { RegisterOrderError } from "../register-order/ui/RegisterOrderError";

interface OrderActionsProps {
  order: OrderRead;
}

export function OrderActions({ order }: OrderActionsProps) {
  const queryClient = useQueryClient();
  const hasItems = order.items.length > 0;

  const mutation = useRegisterOrder({
    onSuccess: async (updatedOrder) => {
      queryClient.setQueryData(["orders", updatedOrder.id], updatedOrder);
      await queryClient.invalidateQueries({
        queryKey: ["orders", updatedOrder.id],
      });
    },
  });

  return (
    <Stack spacing={1}>
      {!hasItems && (
        <Alert severity="warning">
          Добавьте хотя бы одну позицию перед регистрацией заказа.
        </Alert>
      )}

      <RegisterOrderButton
        onClick={() => mutation.mutate(order.id)}
        isPending={mutation.isPending}
        disabled={!hasItems}
      />

      {mutation.isError && <RegisterOrderError />}
    </Stack>
  );
}
