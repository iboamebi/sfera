import { useMemo, useState } from "react";
import { Button, Stack, Typography } from "@mui/material";
import { Link } from "react-router";

import { sortOrders } from "../../features/orders/model/orderSorting";
import type {
  OrderSortCriterion,
} from "../../features/orders/model/orderSorting";
import { useOrders } from "../../features/orders/model/useOrders";
import { OrderListEmpty } from "../../features/orders/ui/OrderListEmpty";
import { OrderListError } from "../../features/orders/ui/OrderListError";
import { OrderListItem } from "../../features/orders/ui/OrderListItem";
import { OrderSortControls } from "../../features/orders/ui/OrderSortControls";

export function OrdersPage() {
  const { data: orders, isLoading, error } = useOrders();
  const [sortCriteria, setSortCriteria] = useState<OrderSortCriterion[]>(
    [],
  );

  const sortedOrders = useMemo(
    () => sortOrders(orders ?? [], sortCriteria),
    [orders, sortCriteria],
  );

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

      <OrderSortControls
        criteria={sortCriteria}
        onChange={setSortCriteria}
      />

      {orders && orders.length === 0 && <OrderListEmpty />}

      {sortedOrders.map((order) => (
        <OrderListItem key={order.id} order={order} />
      ))}
    </Stack>
  );
}
