import { Stack } from "@mui/material";

import { RegisterOrderButton } from "../register-order/ui/RegisterOrderButton";

interface OrderActionsProps {
  orderId: string;
}

export function OrderActions({
  orderId,
}: OrderActionsProps) {
  return (
    <Stack direction="row" spacing={2}>
      <RegisterOrderButton orderId={orderId} />
    </Stack>
  );
}
