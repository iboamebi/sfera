import {
  Alert,
  Button,
  Card,
  CardContent,
  Chip,
  Divider,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";
import { useState } from "react";
import { useQueryClient } from "@tanstack/react-query";

import { AddOrderItemButton } from "../add-order-item/ui/AddOrderItemButton";
import type { OrderRead } from "../model/types";
import { UpdateOrder } from "../update-order/ui/UpdateOrder";
import { useUpdateOrder } from "../update-order/model/useUpdateOrder";
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

const statusColors: Record<string, "default" | "primary" | "warning" | "success"> = {
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

function DetailRow({ label, value }: { label: string; value: string }) {
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
  const queryClient = useQueryClient();
  const [isCommentEditing, setIsCommentEditing] = useState(false);
  const [commentDraft, setCommentDraft] = useState(order.comment ?? "");
  const isEditable = order.status === "NEW";

  const commentMutation = useUpdateOrder({
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["orders", order.id],
      });
      setIsCommentEditing(false);
    },
  });

  const handleCommentSave = () => {
    commentMutation.mutate({
      orderId: order.id,
      data: {
        plannedIssueAt: order.plannedIssueAt ?? undefined,
        comment: commentDraft.trim(),
      },
    });
  };

  const handleCommentCancel = () => {
    setCommentDraft(order.comment ?? "");
    setIsCommentEditing(false);
    commentMutation.reset();
  };

  return (
    <Card>
      <CardContent>
        <Stack spacing={3}>
          <Stack
            direction="row"
            spacing={2}
            sx={{ alignItems: "flex-start", justifyContent: "space-between" }}
          >
            <Stack spacing={0.5}>
              <Typography variant="h5">Заказ № {order.number}</Typography>
              <Typography color="text.secondary" variant="body1">
                {order.customerName}
              </Typography>
            </Stack>
            <Chip
              color={statusColors[order.status] ?? "default"}
              label={statusLabels[order.status] ?? order.status}
            />
          </Stack>

          <Divider />

          <Stack spacing={2}>
            <TableContainer>
              <Table size="small" aria-label="Даты заказа">
                <TableBody>
                  <TableRow>
                    <TableCell sx={{ color: "text.secondary", width: "40%" }}>
                      Создан
                    </TableCell>
                    <TableCell>{formatDate(order.createdAt)}</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell sx={{ color: "text.secondary" }}>
                      Получен
                    </TableCell>
                    <TableCell>{formatDate(order.receivedAt)}</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell sx={{ color: "text.secondary" }}>
                      Изменён
                    </TableCell>
                    <TableCell>{formatDate(order.updatedAt)}</TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </TableContainer>
            <UpdateOrder order={order} />
            <DetailRow label="Выдан" value={formatDate(order.issuedAt)} />
          </Stack>

          <Divider />

          <Stack spacing={1}>
            <Stack
              direction="row"
              spacing={2}
              sx={{ alignItems: "center", justifyContent: "space-between" }}
            >
              <Typography color="text.secondary" variant="body2">
                Комментарий
              </Typography>
              {!isCommentEditing && (
                <Button
                  size="small"
                  variant="text"
                  onClick={() => {
                    setCommentDraft(order.comment ?? "");
                    setIsCommentEditing(true);
                    commentMutation.reset();
                  }}
                >
                  Редактировать
                </Button>
              )}
            </Stack>

            {isCommentEditing ? (
              <Stack spacing={1.5}>
                <TextField
                  fullWidth
                  multiline
                  minRows={3}
                  value={commentDraft}
                  onChange={(event) => setCommentDraft(event.target.value)}
                  disabled={commentMutation.isPending}
                />
                <Stack direction="row" spacing={1}>
                  <Button
                    variant="contained"
                    onClick={handleCommentSave}
                    disabled={commentMutation.isPending}
                  >
                    {commentMutation.isPending ? "Сохранение..." : "Сохранить"}
                  </Button>
                  <Button
                    variant="outlined"
                    onClick={handleCommentCancel}
                    disabled={commentMutation.isPending}
                  >
                    Отмена
                  </Button>
                </Stack>
                {commentMutation.isError && (
                  <Alert severity="error">
                    Не удалось обновить комментарий.
                  </Alert>
                )}
              </Stack>
            ) : (
              <Typography variant="body1" sx={{ whiteSpace: "pre-wrap" }}>
                {order.comment || "—"}
              </Typography>
            )}
          </Stack>

          <Divider />

          <Stack spacing={2}>
            <OrderItems
              items={order.items}
              orderId={order.id}
              customerId={order.customerId}
              editable={isEditable}
            />
            {isEditable && (
              <AddOrderItemButton
                orderId={order.id}
                customerId={order.customerId}
              />
            )}
          </Stack>
        </Stack>
      </CardContent>
    </Card>
  );
}
