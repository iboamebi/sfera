import { useMemo, useState } from "react";
import {
  Button,
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";
import { Link } from "react-router";

import { sortOrders } from "../../features/orders/model/orderSorting";
import type {
  OrderSortCriterion,
  OrderSortField,
} from "../../features/orders/model/orderSorting";
import { useOrders } from "../../features/orders/model/useOrders";
import { OrderListEmpty } from "../../features/orders/ui/OrderListEmpty";
import { OrderListError } from "../../features/orders/ui/OrderListError";
import { OrderListItem } from "../../features/orders/ui/OrderListItem";

const sortableColumns: Array<{
  field: OrderSortField;
  label: string;
}> = [
  { field: "number", label: "Заказ" },
  { field: "createdAt", label: "Дата" },
  { field: "customerName", label: "Клиент" },
  { field: "status", label: "Статус" },
];

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

  const handleSortClick = (field: OrderSortField) => {
    setSortCriteria((current) => {
      const existing = current.find((criterion) => criterion.field === field);

      if (!existing) {
        return [...current, { field, direction: "asc" }];
      }

      if (existing.direction === "asc") {
        return current.map((criterion) =>
          criterion.field === field
            ? { ...criterion, direction: "desc" }
            : criterion,
        );
      }

      return current.filter((criterion) => criterion.field !== field);
    });
  };

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

      {orders && orders.length === 0 && <OrderListEmpty />}

      {orders && orders.length > 0 && sortedOrders.length === 0 && (
        <Typography color="text.secondary">
          По запросу «{search.trim()}» ничего не найдено.
        </Typography>
      )}

      {sortedOrders.length > 0 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small" sx={{ minWidth: 760 }}>
            <TableHead>
              <TableRow>
                {sortableColumns.map(({ field, label }) => {
                  const criterion = sortCriteria.find(
                    (item) => item.field === field,
                  );
                  const priority = sortCriteria.findIndex(
                    (item) => item.field === field,
                  );

                  return (
                    <TableCell
                      key={field}
                      sx={{ fontWeight: 700, whiteSpace: "nowrap" }}
                    >
                      <Button
                        size="small"
                        color="inherit"
                        onClick={() => handleSortClick(field)}
                        aria-label={`Сортировать по полю «${label}»`}
                        sx={{
                          minWidth: 0,
                          px: 0.5,
                          fontWeight: 700,
                          textTransform: "none",
                        }}
                      >
                        {label}
                        {criterion &&
                          ` ${criterion.direction === "asc" ? "↑" : "↓"}`}
                        {criterion && sortCriteria.length > 1 &&
                          ` ${priority + 1}`}
                      </Button>
                    </TableCell>
                  );
                })}
                <TableCell align="right" sx={{ fontWeight: 700 }}>
                  Действие
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {sortedOrders.map((order) => (
                <OrderListItem key={order.id} order={order} />
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Stack>
  );
}
