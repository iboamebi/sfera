import { Stack } from "@mui/material";
import { useQueryClient } from "@tanstack/react-query";

import { useRegisterOrder } from "../register-order/model/useRegisterOrder";
import { RegisterOrderButton } from "../register-order/ui/RegisterOrderButton";
import { RegisterOrderError } from "../register-order/ui/RegisterOrderError";

interface OrderActionsProps {
  orderId: string;
}

export function OrderActions({
  orderId,
}: OrderActionsProps) {
  const queryClient = useQueryClient();

  const mutation = useRegisterOrder({
    onSuccess: (order) => {
      queryClient.setQueryData(
        ["orders", orderId],
        order,
      );
    },
  });

  return (
    <Stack spacing={1}>
      <RegisterOrderButton
        onClick={() => mutation.mutate(orderId)}
        isPending={mutation.isPending}
      />

      {mutation.isError && <RegisterOrderError />}
    </Stack>
  );
}
