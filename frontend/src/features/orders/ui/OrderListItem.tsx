import {
  Button,
  Card,
  CardContent,
  Chip,
  Stack,
  Typography,
} from "@mui/material";
import { Link } from "react-router";

import type { OrderRead } from "../model/types";

interface OrderListItemProps {
  order: OrderRead;
}

const statusLabels: Record<string, string> = {
  NEW: "Новый",
  REGISTERED: "Зарегистрирован",
  IN_WORK: "В работе",
  WAITING: "Ожидание",
  COMPLETED: "Завершён",
  ISSUED: "Выдан",
  CLOSED: "Закрыт",
};

const statusColors: Record<string, "default" | "primary" | "warning" | "success"> = {
  NEW: "default",
  REGISTERED: "primary",
  IN_WORK: "warning",
  WAITING: "warning",
  COMPLETED: "success",
  ISSUED: "success",
  CLOSED: "default",
};

function formatDate(value: string): string {
  return new Intl.DateTimeFormat("ru-RU", {
    dateStyle: "medium",
  }).format(new Date(value));
}

export function OrderListItem({ order }: OrderListItemProps) {
  return (
    <Card variant="outlined">
      <CardContent>
        <Stack
          direction={{ xs: "column", sm: "row" }}
          spacing={2}
          sx={{
            alignItems: { xs: "stretch", sm: "center" },
            justifyContent: "space-between",
          }}
        >
          <Stack spacing={1} sx={{ minWidth: 0 }}>
            <Typography variant="h6">
              Заказ № {order.number}
            </Typography>
            <Typography color="text.secondary" variant="body2">
              Клиент: {order.customerName}
            </Typography>
            <Typography color="text.secondary" variant="body2">
              Создан: {formatDate(order.createdAt)}
            </Typography>
          </Stack>

          <Stack
            direction="row"
            spacing={1}
            sx={{ alignItems: "center", flexWrap: "wrap" }}
          >
            <Chip
              size="small"
              color={statusColors[order.status] ?? "default"}
              label={statusLabels[order.status] ?? order.status}
            />
            <Button
              component={Link}
              to={`/orders/${order.id}`}
              variant="outlined"
              size="small"
            >
              Открыть / редактировать
            </Button>
          </Stack>
        </Stack>
      </CardContent>
    </Card>
  );
}
