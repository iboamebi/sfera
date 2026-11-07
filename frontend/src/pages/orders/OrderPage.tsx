import {
  Button,
  Card,
  CardContent,
  Stack,
  Typography,
} from "@mui/material";
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
    <Stack spacing={3}>
      <Button
        variant="outlined"
        onClick={() => navigate("/orders")}
        sx={{ alignSelf: "flex-start" }}
      >
        Назад
      </Button>

      <OrderDetails order={data} />

      <Card variant="outlined">
        <CardContent>
          <Stack spacing={1.5}>
            <Typography variant="h6">Регистрация заказа</Typography>
            <Typography color="text.secondary" variant="body2">
              Отдельное действие: переводит заказ в зарегистрированное состояние.
            </Typography>
            <OrderActions order={data} />
          </Stack>
        </CardContent>
      </Card>

      <Card variant="outlined">
        <CardContent>
          <Stack spacing={2}>
            <Typography variant="h6">Параметры заказа</Typography>
            <Typography color="text.secondary" variant="body2">
              Здесь можно изменить планируемую дату выдачи и комментарий.
            </Typography>
            <UpdateOrder order={data} />
          </Stack>
        </CardContent>
      </Card>
    </Stack>
  );
}
