import {
  Alert,
  Button,
  Chip,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Divider,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import { useState } from "react";

import { useUpdateDevice } from "../../devices/model/useUpdateDevice";
import { DeleteOrderItemButton } from "../delete-order-item/ui/DeleteOrderItemButton";
import type { OrderItem, OrderItemOperation } from "../model/types";

interface OrderItemsProps {
  items: OrderItem[];
  deletingItemId?: string | null;
  onDelete?: (itemId: string) => void;
}

const OPERATION_LABELS: Record<OrderItemOperation, string> = {
  verification: "Поверка",
  diagnostic: "Диагностика",
  repair: "Ремонт",
  sale: "Продажа",
};

export function OrderItems({
  items,
  deletingItemId = null,
  onDelete,
}: OrderItemsProps) {
  const [editingItem, setEditingItem] = useState<OrderItem | null>(null);
  const [serialNumber, setSerialNumber] = useState("");
  const [modification, setModification] = useState("");
  const updateDeviceMutation = useUpdateDevice();

  const openEditor = (item: OrderItem) => {
    if (!item.instrumentId) {
      return;
    }

    setEditingItem(item);
    setSerialNumber(item.serialNumber ?? "");
    setModification(item.modification ?? "");
    updateDeviceMutation.reset();
  };

  const closeEditor = () => {
    if (!updateDeviceMutation.isPending) {
      setEditingItem(null);
    }
  };

  const saveDevice = () => {
    if (
      !editingItem?.instrumentId ||
      !editingItem.instrumentTypeId ||
      !serialNumber.trim()
    ) {
      return;
    }

    updateDeviceMutation.mutate(
      {
        deviceId: editingItem.instrumentId,
        instrumentTypeId: editingItem.instrumentTypeId,
        serialNumber: serialNumber.trim(),
        modification: modification.trim() || null,
      },
      {
        onSuccess: () => setEditingItem(null),
      },
    );
  };

  return (
    <Stack spacing={2}>
      <Typography variant="h6">Позиции заказа</Typography>

      {items.length === 0 ? (
        <Typography color="text.secondary" variant="body2">
          Позиции отсутствуют
        </Typography>
      ) : (
        items.map((item, index) => (
          <Stack key={item.id} spacing={0.5}>
            <Stack
              direction="row"
              sx={{
                alignItems: "center",
                justifyContent: "space-between",
              }}
            >
              <Typography variant="body1">Позиция {index + 1}</Typography>

              <Stack direction="row" spacing={1}>
                {item.instrumentId && (
                  <Button size="small" onClick={() => openEditor(item)}>
                    Редактировать СИ
                  </Button>
                )}

                {onDelete && (
                  <DeleteOrderItemButton
                    isPending={deletingItemId === item.id}
                    onClick={() => onDelete(item.id)}
                  />
                )}
              </Stack>
            </Stack>

            <Typography color="text.secondary" variant="body2">
              {item.instrumentTypeName ?? "СИ"}: {item.serialNumber ?? "—"}
            </Typography>

            {item.modification && (
              <Typography color="text.secondary" variant="body2">
                Модификация: {item.modification}
              </Typography>
            )}

            <Stack direction="row" sx={{ flexWrap: "wrap", gap: 0.5 }}>
              {item.requestedOperations.map((operation) => (
                <Chip
                  key={operation}
                  label={OPERATION_LABELS[operation]}
                  size="small"
                />
              ))}
            </Stack>

            <Typography variant="body2">{item.comment || "—"}</Typography>

            {index < items.length - 1 && <Divider sx={{ pt: 1 }} />}
          </Stack>
        ))
      )}

      <Dialog open={editingItem !== null} onClose={closeEditor} fullWidth maxWidth="sm">
        <DialogTitle>Редактирование СИ</DialogTitle>
        <DialogContent>
          <Stack spacing={2} sx={{ pt: 1 }}>
            <Typography color="text.secondary" variant="body2">
              {editingItem?.instrumentTypeName ?? "СИ"}
            </Typography>

            <TextField
              label="Серийный номер"
              value={serialNumber}
              onChange={(event) => setSerialNumber(event.target.value)}
              required
              fullWidth
            />

            <TextField
              label="Модификация"
              value={modification}
              onChange={(event) => setModification(event.target.value)}
              fullWidth
            />

            {!editingItem?.instrumentTypeId && (
              <Alert severity="warning">
                Для этой позиции не указан тип СИ, поэтому сохранить карточку пока нельзя.
              </Alert>
            )}

            {updateDeviceMutation.isError && (
              <Alert severity="error">
                Не удалось сохранить карточку СИ.
              </Alert>
            )}
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={closeEditor} disabled={updateDeviceMutation.isPending}>
            Отмена
          </Button>
          <Button
            variant="contained"
            onClick={saveDevice}
            disabled={
              !serialNumber.trim() ||
              !editingItem?.instrumentTypeId ||
              updateDeviceMutation.isPending
            }
          >
            Сохранить
          </Button>
        </DialogActions>
      </Dialog>
    </Stack>
  );
}
