import { Button, Stack, Typography } from "@mui/material";
import { useNavigate, useParams } from "react-router";

import { UpdateOrder } from "../../features/orders/update-order/ui/UpdateOrder";
import { useOrder } from "../../features/orders/model/useOrder";
import { OrderActions } from "../../features/orders/ui/OrderActions";
import { OrderDetails } from "../../features/orders/ui/OrderDetails";
import { OrderError } from "../../features/orders/ui/OrderError";

export function OrderPage() {
  const { orderId } = useParams<{ orderId: string }>();
  const navigate = useNavigate();
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
      <Button
        variant="outlined"
        onClick={() => navigate("/orders")}
        sx={{ alignSelf: "flex-start" }}
      >
        Назад
      </Button>
      <OrderDetails order={data} />
      <OrderActions order={data} />
      <UpdateOrder order={data} />
    </Stack>
  );
}
