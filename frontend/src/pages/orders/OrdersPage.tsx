import { Alert, Button, Stack, Typography } from "@mui/material";
import { Link } from "react-router";

import { useOrders } from "../../features/orders/model/useOrders";

export function OrdersPage() {
  const { data: orders, isLoading, error } = useOrders();

  if (isLoading) {
    return <Typography>Loading orders...</Typography>;
  }

  if (error) {
    return <Alert severity="error">Failed to load orders.</Alert>;
  }

  return (
    <Stack spacing={2}>
      <Button component={Link} to="/orders/new" variant="contained">
        Создать заказ
      </Button>

      {orders?.map((order) => (
        <Stack key={order.id} spacing={1}>
          <Typography>
            {order.number} — {order.status}
          </Typography>

          <Button
            component={Link}
            to={`/orders/${order.id}`}
            variant="outlined"
          >
            Открыть
          </Button>
        </Stack>
      ))}
    </Stack>
  );
}
