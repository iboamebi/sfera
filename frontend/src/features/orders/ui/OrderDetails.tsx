import {
  Card,
  CardContent,
  Chip,
  Divider,
  Stack,
  Typography,
} from "@mui/material";

import type { OrderRead } from "../model/types";
import { AddOrderItemButton } from "../add-order-item/ui/AddOrderItemButton";
import { OrderItems } from "./OrderItems";

interface OrderDetailsProps {
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

const statusColors: Record<
  string,
  "default" | "primary" | "warning" | "success"
> = {
  NEW: "default",
  REGISTERED: "primary",
  IN_WORK: "warning",
  WAITING: "warning",
  COMPLETED: "success",
  ISSUED: "success",
  CLOSED: "default",
};

function formatDate(value: string | null): string {
  if (!value) {
    return "—";
  }

  return new Intl.DateTimeFormat("ru-RU", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

function DetailRow({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <Stack spacing={0.5}>
      <Typography color="text.secondary" variant="body2">
        {label}
      </Typography>

      <Typography variant="body1">{value}</Typography>
    </Stack>
  );
}

export function OrderDetails({ order }: OrderDetailsProps) {
  return (
    <Card>
      <CardContent>
        <Stack spacing={3}>
          <Stack
            direction="row"
            spacing={2}
            sx={{
              alignItems: "flex-start",
              justifyContent: "space-between",
            }}
          >
            <Typography variant="h5">Заказ № {order.number}</Typography>

            <Chip
              color={statusColors[order.status] ?? "default"}
              label={statusLabels[order.status] ?? order.status}
            />
          </Stack>

          <Divider />

          <Stack spacing={2}>
            <DetailRow label="Клиент" value={order.customerId} />

            <DetailRow label="Получен" value={formatDate(order.receivedAt)} />

            <DetailRow
              label="Планируемая выдача"
              value={formatDate(order.plannedIssueAt)}
            />

            <DetailRow label="Выдан" value={formatDate(order.issuedAt)} />
          </Stack>

          <Divider />

          <Stack spacing={0.5}>
            <Typography color="text.secondary" variant="body2">
              Комментарий
            </Typography>

            <Typography variant="body1">{order.comment || "—"}</Typography>
          </Stack>

          <Divider />

          <Stack
            direction="row"
            spacing={2}
            sx={{ alignItems: "center", justifyContent: "space-between" }}
          >
            <OrderItems items={order.items} />
            <AddOrderItemButton orderId={order.id} />
          </Stack>
        </Stack>
      </CardContent>
    </Card>
  );
}
