import {
  Chip,
  TableCell,
  TableRow,
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
    <TableRow hover>
      <TableCell sx={{ whiteSpace: "nowrap" }}>
        <Typography
          component={Link}
          to={`/orders/${order.id}`}
          sx={{
            color: "primary.main",
            fontWeight: 600,
            textDecoration: "none",
            "&:hover": { textDecoration: "underline" },
          }}
        >
          № {order.number}
        </Typography>
      </TableCell>
      <TableCell sx={{ whiteSpace: "nowrap" }}>
        {formatDate(order.createdAt)}
      </TableCell>
      <TableCell>{order.customerName}</TableCell>
      <TableCell>
        <Chip
          size="small"
          color={statusColors[order.status] ?? "default"}
          label={statusLabels[order.status] ?? order.status}
        />
      </TableCell>
    </TableRow>
  );
}
