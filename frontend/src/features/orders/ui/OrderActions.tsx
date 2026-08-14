import { Stack } from "@mui/material";

import { useRegisterOrder } from "../register-order/model/useRegisterOrder";
import { RegisterOrderButton } from "../register-order/ui/RegisterOrderButton";
import { RegisterOrderError } from "../register-order/ui/RegisterOrderError";

interface OrderActionsProps {
  orderId: string;
}

export function OrderActions({
  orderId,
}: OrderActionsProps) {
  const mutation = useRegisterOrder();

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
