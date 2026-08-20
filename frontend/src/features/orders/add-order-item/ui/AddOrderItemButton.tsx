import { Button } from "@mui/material";

import { useAddOrderItem } from "../model/useAddOrderItem";

interface AddOrderItemButtonProps {
  orderId: string;
}

export function AddOrderItemButton({ orderId }: AddOrderItemButtonProps) {
  const mutation = useAddOrderItem(orderId);

  return (
    <Button
      disabled={mutation.isPending}
      onClick={() => mutation.mutate(null)}
      variant="outlined"
    >
      {mutation.isPending ? "Добавление…" : "Добавить позицию"}
    </Button>
  );
}
