import { Button, Stack, Typography } from "@mui/material";
import { Link } from "react-router";

import { useOrders } from "../../features/orders/model/useOrders";
import { OrderListEmpty } from "../../features/orders/ui/OrderListEmpty";
import { OrderListError } from "../../features/orders/ui/OrderListError";
import { OrderListItem } from "../../features/orders/ui/OrderListItem";

export function OrdersPage() {
  const { data: orders, isLoading, error } = useOrders();

  if (isLoading) {
    return <Typography>Loading orders...</Typography>;
  }

  if (error) {
    return <OrderListError />;
  }

  return (
    <Stack spacing={2}>
      <Button component={Link} to="/orders/new" variant="contained">
        Создать заказ
      </Button>

      {orders && orders.length === 0 && <OrderListEmpty />}

      {orders?.map((order) => (
        <OrderListItem key={order.id} order={order} />
      ))}
    </Stack>
  );
}
