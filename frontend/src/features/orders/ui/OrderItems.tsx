import {
  Alert,
  Button,
  Chip,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Divider,
  MenuItem,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import { useState } from "react";

import { useCreateDevice } from "../../devices/model/useCreateDevice";
import { useDevices } from "../../devices/model/useDevices";
import { useUpdateDevice } from "../../devices/model/useUpdateDevice";
import { DeleteOrderItemButton } from "../delete-order-item/ui/DeleteOrderItemButton";
import { useAssignOrderItemInstrument } from "../model/useAssignOrderItemInstrument";
import type { OrderItem, OrderItemOperation } from "../model/types";

interface OrderItemsProps {
  items: OrderItem[];
  orderId?: string;
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
  orderId = "",
  deletingItemId = null,
  onDelete,
}: OrderItemsProps) {
  const [editingItem, setEditingItem] = useState<OrderItem | null>(null);
  const [selectedInstrumentId, setSelectedInstrumentId] = useState("");
  const [serialNumber, setSerialNumber] = useState("");
  const [modification, setModification] = useState("");
  const updateDeviceMutation = useUpdateDevice();
  const createDeviceMutation = useCreateDevice();
  const assignMutation = useAssignOrderItemInstrument(orderId);
  const devicesQuery = useDevices();

  const openEditor = (item: OrderItem) => {
    setEditingItem(item);
    setSelectedInstrumentId(item.instrumentId ?? "");
    setSerialNumber(item.serialNumber ?? "");
    setModification(item.modification ?? "");
    updateDeviceMutation.reset();
    createDeviceMutation.reset();
    assignMutation.reset();
  };

  const closeEditor = () => {
    if (!updateDeviceMutation.isPending && !createDeviceMutation.isPending && !assignMutation.isPending) {
      setEditingItem(null);
    }
  };

  const saveDevice = () => {
    if (!editingItem?.instrumentTypeId || !serialNumber.trim()) {
      return;
    }

    if (editingItem.instrumentId) {
      updateDeviceMutation.mutate(
        {
          deviceId: editingItem.instrumentId,
          instrumentTypeId: editingItem.instrumentTypeId,
          serialNumber: serialNumber.trim(),
          modification: modification.trim() || null,
        },
        { onSuccess: () => setEditingItem(null) },
      );
      return;
    }

    if (selectedInstrumentId) {
      assignMutation.mutate(
        { itemId: editingItem.id, instrumentId: selectedInstrumentId },
        { onSuccess: () => setEditingItem(null) },
      );
      return;
    }

    createDeviceMutation.mutate(
      {
        instrumentTypeId: editingItem.instrumentTypeId,
        serialNumber: serialNumber.trim(),
      },
      {
        onSuccess: (device) => {
          assignMutation.mutate(
            { itemId: editingItem.id, instrumentId: device.id },
            { onSuccess: () => setEditingItem(null) },
          );
        },
      },
    );
  };

  const matchingDevices = devicesQuery.data?.filter(
    (device) => device.instrumentTypeId === editingItem?.instrumentTypeId,
  ) ?? [];

  return (
    <Stack spacing={2}>
      <Typography variant="h6">Позиции заказа</Typography>
      {items.length === 0 ? (
        <Typography color="text.secondary" variant="body2">Позиции отсутствуют</Typography>
      ) : (
        items.map((item, index) => (
          <Stack key={item.id} spacing={0.5}>
            <Stack direction="row" sx={{ alignItems: "center", justifyContent: "space-between" }}>
              <Typography variant="body1">Позиция {index + 1}</Typography>
              <Stack direction="row" spacing={1}>
                <Button size="small" onClick={() => openEditor(item)}>
                  Редактировать СИ
                </Button>
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
              <Typography color="text.secondary" variant="body2">Модификация: {item.modification}</Typography>
            )}
            <Stack direction="row" sx={{ flexWrap: "wrap", gap: 0.5 }}>
              {item.requestedOperations.map((operation) => (
                <Chip key={operation} label={OPERATION_LABELS[operation]} size="small" />
              ))}
            </Stack>
            <Typography variant="body2">{item.comment || "—"}</Typography>
            {index < items.length - 1 && <Divider sx={{ pt: 1 }} />}
          </Stack>
        ))
      )}

      <Dialog open={editingItem !== null} onClose={closeEditor} fullWidth maxWidth="sm">
        <DialogTitle>{editingItem?.instrumentId ? "Редактирование СИ" : "Идентификация СИ"}</DialogTitle>
        <DialogContent>
          <Stack spacing={2} sx={{ pt: 1 }}>
            <Typography color="text.secondary" variant="body2">{editingItem?.instrumentTypeName ?? "СИ"}</Typography>

            {!editingItem?.instrumentId && (
              <TextField
                select
                label="Известное СИ"
                value={selectedInstrumentId}
                onChange={(event) => setSelectedInstrumentId(event.target.value)}
                fullWidth
              >
                <MenuItem value="">Новое СИ</MenuItem>
                {matchingDevices.map((device) => (
                  <MenuItem key={device.id} value={device.id}>
                    {device.serialNumber}
                  </MenuItem>
                ))}
              </TextField>
            )}

            <TextField
              label="Серийный номер"
              value={serialNumber}
              onChange={(event) => setSerialNumber(event.target.value)}
              required
              fullWidth
              disabled={Boolean(selectedInstrumentId)}
            />
            <TextField
              label="Модификация"
              value={modification}
              onChange={(event) => setModification(event.target.value)}
              fullWidth
              disabled={Boolean(selectedInstrumentId)}
            />

            {devicesQuery.isError && !editingItem?.instrumentId && (
              <Alert severity="warning">Не удалось загрузить список известных СИ. Можно создать новое СИ.</Alert>
            )}
            {(updateDeviceMutation.isError || createDeviceMutation.isError || assignMutation.isError) && (
              <Alert severity="error">Не удалось сохранить карточку СИ.</Alert>
            )}
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={closeEditor} disabled={updateDeviceMutation.isPending || createDeviceMutation.isPending || assignMutation.isPending}>Отмена</Button>
          <Button
            variant="contained"
            onClick={saveDevice}
            disabled={(!selectedInstrumentId && !serialNumber.trim()) || !editingItem?.instrumentTypeId || updateDeviceMutation.isPending || createDeviceMutation.isPending || assignMutation.isPending}
          >
            Сохранить
          </Button>
        </DialogActions>
      </Dialog>
    </Stack>
  );
}
