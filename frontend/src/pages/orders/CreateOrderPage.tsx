import { Alert } from "@mui/material";
import { useNavigate } from "react-router-dom";

import { useCreateOrder } from "../../features/orders/create-order/model/useCreateOrder";
import { CreateOrderForm } from "../../features/orders/create-order/ui/CreateOrderForm";

export function CreateOrderPage() {
  const navigate = useNavigate();
  const { mutate, isPending, error } = useCreateOrder({
    onSuccess: (order) => {
      navigate(`/orders/${order.id}`);
    },
  });

  return (
    <>
      {error && <Alert severity="error">Failed to create order.</Alert>}
      <CreateOrderForm onSubmit={mutate} isPending={isPending} />
    </>
  );
}
