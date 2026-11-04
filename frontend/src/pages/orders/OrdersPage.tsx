import { useMemo, useState } from "react";
import {
  Button,
  Paper,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
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
  const [sortCriteria, setSortCriteria] = useState<OrderSortCriterion[]>([]);
  const [search, setSearch] = useState("");

  const filteredOrders = useMemo(() => {
    const query = search.trim().toLocaleLowerCase("ru-RU");

    if (!query) {
      return orders ?? [];
    }

    return (orders ?? []).filter((order) =>
      [order.number, order.customerName, order.status]
        .some((value) => value.toLocaleLowerCase("ru-RU").includes(query)),
    );
  }, [orders, search]);

  const sortedOrders = useMemo(
    () => sortOrders(filteredOrders, sortCriteria),
    [filteredOrders, sortCriteria],
  );

  if (isLoading) {
    return <Typography>Загрузка заказов...</Typography>;
  }

  if (error) {
    return <OrderListError />;
  }

  return (
    <Stack spacing={3}>
      <Stack
        direction="row"
        spacing={2}
        sx={{
          alignItems: { xs: "stretch", sm: "center" },
          justifyContent: "space-between",
          flexWrap: "wrap",
        }}
      >
        <Typography variant="h4">Заказы</Typography>
        <Button component={Link} to="/orders/new" variant="contained">
          Создать заказ
        </Button>
      </Stack>

      <TextField
        label="Поиск заказов"
        placeholder="Номер, клиент или статус"
        value={search}
        onChange={(event) => setSearch(event.target.value)}
        size="small"
        fullWidth
      />

      <Paper variant="outlined" sx={{ p: 2 }}>
        <OrderSortControls
          criteria={sortCriteria}
          onChange={setSortCriteria}
        />
      </Paper>

      {orders && orders.length === 0 && <OrderListEmpty />}

      {orders && orders.length > 0 && sortedOrders.length === 0 && (
        <Typography color="text.secondary">
          По запросу «{search.trim()}» ничего не найдено.
        </Typography>
      )}

      <Stack spacing={1.5}>
        {sortedOrders.map((order) => (
          <OrderListItem key={order.id} order={order} />
        ))}
      </Stack>
    </Stack>
  );
}
