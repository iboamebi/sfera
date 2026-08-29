import { Button, Stack } from "@mui/material";
import { useNavigate } from "react-router";

import { useCreateOrder } from "../../features/orders/create-order/model/useCreateOrder";
import { CreateOrderError } from "../../features/orders/create-order/ui/CreateOrderError";
import { CreateOrderForm } from "../../features/orders/create-order/ui/CreateOrderForm";

export function CreateOrderPage() {
  const navigate = useNavigate();
  const { mutate, isPending, error } = useCreateOrder({
    onSuccess: (order) => {
      navigate(`/orders/${order.id}`);
    },
  });

  return (
    <Stack spacing={2}>
      <Button
        onClick={() => navigate("/orders")}
        sx={{ alignSelf: "flex-start" }}
        variant="text"
      >
        К списку заказов
      </Button>

      {error && <CreateOrderError />}
      <CreateOrderForm onSubmit={mutate} isPending={isPending} />
    </Stack>
  );
}
