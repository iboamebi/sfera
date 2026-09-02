import { useState } from "react";

import { Button, Checkbox, Chip, Divider, FormControlLabel, Stack, Typography } from "@mui/material";
import { useNavigate } from "react-router";

import { useAssignOrderItemInstrument } from "../add-order-item/model/useAssignOrderItemInstrument";
import { useDeleteOrderItem } from "../add-order-item/model/useDeleteOrderItem";
import { useUpdateOrderItem } from "../add-order-item/model/useUpdateOrderItem";
import { DeviceSelector } from "../add-order-item/ui/DeviceSelector";
import type { OrderItem, OrderItemOperation } from "../model/types";

interface OrderItemsProps {
  items: OrderItem[];
  orderId: string;
  editable?: boolean;
}

const OPERATION_LABELS: Record<OrderItemOperation, string> = {
  verification: "Поверка",
  diagnostic: "Диагностика",
  repair: "Ремонт",
  sale: "Продажа",
};

const OPERATION_OPTIONS = Object.entries(OPERATION_LABELS) as Array<
  [OrderItemOperation, string]
>;

export function OrderItems({ items, orderId, editable = false }: OrderItemsProps) {
  const navigate = useNavigate();
  const updateMutation = useUpdateOrderItem(orderId);
  const assignInstrumentMutation = useAssignOrderItemInstrument(orderId);
  const deleteMutation = useDeleteOrderItem(orderId);
  const [editingItemId, setEditingItemId] = useState<string | null>(null);
  const [editedOperations, setEditedOperations] = useState<OrderItemOperation[]>([]);
  const [assigningItemId, setAssigningItemId] = useState<string | null>(null);
  const [selectedInstrumentId, setSelectedInstrumentId] = useState("");

  const startEditing = (item: OrderItem) => {
    setEditingItemId(item.id);
    setEditedOperations(item.requestedOperations);
  };

  const toggleOperation = (operation: OrderItemOperation) => {
    setEditedOperations((current) =>
      current.includes(operation)
        ? current.filter((value) => value !== operation)
        : [...current, operation],
    );
  };

  const saveEdit = (itemId: string) => {
    updateMutation.mutate(
      { itemId, requestedOperations: editedOperations },
      { onSuccess: () => setEditingItemId(null) },
    );
  };

  const removeItem = (itemId: string) => {
    if (!window.confirm("Удалить позицию заказа?")) {
      return;
    }
    deleteMutation.mutate(itemId);
  };

  const openDeviceCard = (instrumentId: string | null) => {
    if (!instrumentId) {
      return;
    }
    navigate(`/devices/${instrumentId}?edit=1&returnToOrder=${orderId}`);
  };

  const startAssigningInstrument = (item: OrderItem) => {
    setAssigningItemId(item.id);
    setSelectedInstrumentId("");
  };

  const cancelAssigningInstrument = () => {
    setAssigningItemId(null);
    setSelectedInstrumentId("");
  };

  const saveInstrumentAssignment = (itemId: string) => {
    if (!selectedInstrumentId) {
      return;
    }

    assignInstrumentMutation.mutate(
      { itemId, instrumentId: selectedInstrumentId },
      {
        onSuccess: () => {
          setAssigningItemId(null);
          setSelectedInstrumentId("");
        },
      },
    );
  };

  return (
    <Stack spacing={2} sx={{ width: "100%" }}>
      <Typography variant="h6">Позиции заказа</Typography>

      {items.length === 0 ? (
        <Typography color="text.secondary" variant="body2">
          Позиции отсутствуют
        </Typography>
      ) : (
        items.map((item, index) => (
          <Stack key={item.id} spacing={0.5}>
            <Typography variant="body1">Позиция {index + 1}</Typography>

            <Stack spacing={0.25}>
              <Typography color="text.secondary" variant="body2">
                Наименование СИ: {item.instrumentName ?? "—"}
              </Typography>
              <Typography color="text.secondary" variant="body2">
                Тип СИ: {item.instrumentTypeName ?? "—"}
              </Typography>
              <Typography color="text.secondary" variant="body2">
                Модель СИ: {item.modification ?? "—"}
              </Typography>
              <Typography color="text.secondary" variant="body2">
                Заводской номер: {item.serialNumber ?? "—"}
              </Typography>
            </Stack>

            {editable && !item.instrumentId && assigningItemId === item.id && (
              <Stack spacing={1}>
                <DeviceSelector
                  value={selectedInstrumentId}
                  instrumentTypeId={item.instrumentTypeId}
                  onChange={setSelectedInstrumentId}
                />
                <Stack direction="row" spacing={1}>
                  <Button
                    size="small"
                    variant="contained"
                    disabled={
                      assignInstrumentMutation.isPending || !selectedInstrumentId
                    }
                    onClick={() => saveInstrumentAssignment(item.id)}
                  >
                    Назначить СИ
                  </Button>
                  <Button
                    size="small"
                    disabled={assignInstrumentMutation.isPending}
                    onClick={cancelAssigningInstrument}
                  >
                    Отмена
                  </Button>
                </Stack>
              </Stack>
            )}

            {item.instrumentId && (
              <Stack direction="row">
                <Button
                  size="small"
                  variant="outlined"
                  onClick={() => openDeviceCard(item.instrumentId)}
                >
                  Редактировать карту СИ
                </Button>
              </Stack>
            )}

            {editable && !item.instrumentId && assigningItemId !== item.id && (
              <Stack direction="row">
                <Button
                  size="small"
                  variant="outlined"
                  onClick={() => startAssigningInstrument(item)}
                >
                  Назначить СИ
                </Button>
              </Stack>
            )}

            {editingItemId === item.id ? (
              <Stack direction="row" sx={{ flexWrap: "wrap" }}>
                {OPERATION_OPTIONS.map(([operation, label]) => (
                  <FormControlLabel
                    key={operation}
                    control={
                      <Checkbox
                        checked={editedOperations.includes(operation)}
                        onChange={() => toggleOperation(operation)}
                      />
                    }
                    label={label}
                  />
                ))}
              </Stack>
            ) : (
              <Stack direction="row" sx={{ flexWrap: "wrap", gap: 0.5 }}>
                {item.requestedOperations.map((operation) => (
                  <Chip
                    key={operation}
                    label={OPERATION_LABELS[operation]}
                    size="small"
                  />
                ))}
              </Stack>
            )}

            <Typography variant="body2">{item.comment || "—"}</Typography>

            {editable && (
              <Stack direction="row" spacing={1}>
                {editingItemId === item.id ? (
                  <>
                    <Button
                      size="small"
                      variant="contained"
                      disabled={updateMutation.isPending || editedOperations.length === 0}
                      onClick={() => saveEdit(item.id)}
                    >
                      Сохранить
                    </Button>
                    <Button
                      size="small"
                      disabled={updateMutation.isPending}
                      onClick={() => setEditingItemId(null)}
                    >
                      Отмена
                    </Button>
                  </>
                ) : (
                  <>
                    <Button size="small" onClick={() => startEditing(item)}>
                      Изменить
                    </Button>
                    <Button
                      size="small"
                      color="error"
                      disabled={deleteMutation.isPending}
                      onClick={() => removeItem(item.id)}
                    >
                      Удалить
                    </Button>
                  </>
                )}
              </Stack>
            )}

            {index < items.length - 1 && <Divider sx={{ pt: 1 }} />}
          </Stack>
        ))
      )}
    </Stack>
  );
}
