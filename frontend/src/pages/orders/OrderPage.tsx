import { Stack, Typography } from "@mui/material";
import { useParams } from "react-router";

import { AddOrderItemsForm } from "../../features/orders/add-order-items/ui/AddOrderItemsForm";
import { UpdateOrder } from "../../features/orders/update-order/ui/UpdateOrder";
import { useOrder } from "../../features/orders/model/useOrder";
import { OrderActions } from "../../features/orders/ui/OrderActions";
import { OrderDetails } from "../../features/orders/ui/OrderDetails";
import { OrderError } from "../../features/orders/ui/OrderError";

export function OrderPage() {
  const { orderId } = useParams<{ orderId: string }>();
  const { data, error, isLoading } = useOrder(orderId ?? "");

  if (isLoading) {
    return <Typography>Loading...</Typography>;
  }

  if (error) {
    return <OrderError />;
  }

  if (!data) {
    return null;
  }

  return (
    <Stack spacing={2}>
      <OrderDetails order={data} />
      <OrderActions order={data} />
      <AddOrderItemsForm orderId={data.id} />
      <UpdateOrder order={data} />
    </Stack>
  );
}
