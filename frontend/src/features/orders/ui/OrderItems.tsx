import { Alert, Button, Chip, Dialog, DialogActions, DialogContent, DialogTitle, Divider, MenuItem, Stack, TextField, Typography } from "@mui/material";
import { useMemo, useState } from "react";

import { useAssignOrderItemInstrument } from "../model/useAssignOrderItemInstrument";
import { useDevices } from "../../devices/model/useDevices";
import { useCreateDevice } from "../../devices/model/useCreateDevice";
import { useUpdateDevice } from "../../devices/model/useUpdateDevice";
import type { DeviceRead } from "../../devices/model/types";
import type { OrderItem } from "../model/types";

const OPERATION_LABELS: Record<string, string> = {
  verification: "Поверка",
  repair: "Ремонт",
  diagnostics: "Диагностика",
};

interface OrderItemsProps {
  orderId: string;
  items: OrderItem[];
  deletingItemId?: string | null;
  onDelete?: (itemId: string) => void;
}

export function OrderItems({ orderId, items, deletingItemId, onDelete }: OrderItemsProps) {
  const [editingItem, setEditingItem] = useState<OrderItem | null>(null);
  const [serialNumber, setSerialNumber] = useState("");
  const [registryNumber, setRegistryNumber] = useState("");
  const [modification, setModification] = useState("");
  const [factoryNumber, setFactoryNumber] = useState("");
  const [manufactureYear, setManufactureYear] = useState("");
  const [inventoryNumber, setInventoryNumber] = useState("");
  const [comment, setComment] = useState("");
  const [selectedInstrumentId, setSelectedInstrumentId] = useState("");

  const devicesQuery = useDevices();
  const createDeviceMutation = useCreateDevice();
  const updateDeviceMutation = useUpdateDevice(orderId);
  const assignMutation = useAssignOrderItemInstrument(orderId);

  const matchingDevices = useMemo<DeviceRead[]>(() => {
    if (!editingItem?.instrumentTypeId) return [];
    return (devicesQuery.data ?? []).filter(
      (device) => device.instrumentTypeId === editingItem.instrumentTypeId,
    );
  }, [devicesQuery.data, editingItem?.instrumentTypeId]);

  const openEditor = (item: OrderItem) => {
    setEditingItem(item);
    setSerialNumber(item.serialNumber ?? "");
    setRegistryNumber(item.registryNumber ?? "");
    setModification(item.modification ?? "");
    setFactoryNumber(item.factoryNumber ?? "");
    setManufactureYear(item.manufactureYear?.toString() ?? "");
    setInventoryNumber(item.inventoryNumber ?? "");
    setComment(item.comment ?? "");
    setSelectedInstrumentId(item.instrumentId ?? "");
  };

  const closeEditor = () => setEditingItem(null);

  const selectKnownDevice = (deviceId: string) => {
    setSelectedInstrumentId(deviceId);
    const device = matchingDevices.find((item) => item.id === deviceId);
    if (!device) return;
    setSerialNumber(device.serialNumber ?? "");
    setRegistryNumber(device.registryNumber ?? "");
    setModification(device.modification ?? "");
    setFactoryNumber(device.factoryNumber ?? "");
    setManufactureYear(device.manufactureYear?.toString() ?? "");
    setInventoryNumber(device.inventoryNumber ?? "");
    setComment(device.comment ?? "");
  };

  const saveDevice = async () => {
    if (!editingItem?.instrumentTypeId) return;

    const payload = {
      instrumentTypeId: editingItem.instrumentTypeId,
      serialNumber: serialNumber.trim(),
      registryNumber: registryNumber.trim() || null,
      modification: modification.trim() || null,
      factoryNumber: factoryNumber.trim() || null,
      manufactureYear: manufactureYear ? Number(manufactureYear) : null,
      inventoryNumber: inventoryNumber.trim() || null,
      comment: comment.trim() || null,
    };

    if (selectedInstrumentId) {
      await updateDeviceMutation.mutateAsync({ deviceId: selectedInstrumentId, ...payload });
      await assignMutation.mutateAsync({ itemId: editingItem.id, instrumentId: selectedInstrumentId });
    } else {
      const device = await createDeviceMutation.mutateAsync(payload);
      await assignMutation.mutateAsync({ itemId: editingItem.id, instrumentId: device.id });
    }

    closeEditor();
  };

  const isPending =
    createDeviceMutation.isPending || updateDeviceMutation.isPending || assignMutation.isPending;

  return (
    <Stack spacing={2}>
      {items.map((item, index) => (
        <Stack key={item.id} spacing={1}>
          <Stack direction="row" sx={{ alignItems: "center", justifyContent: "space-between" }}>
            <Typography variant="subtitle1">
              {item.instrumentTypeName || "Позиция заказа"}
            </Typography>
            <Stack direction="row" spacing={1}>
              <Button size="small" onClick={() => openEditor(item)}>
                Редактировать
              </Button>
              {onDelete && (
                <Button
                  size="small"
                  color="error"
                  onClick={() => onDelete(item.id)}
                  disabled={deletingItemId === item.id}
                >
                  {deletingItemId === item.id ? "Удаление…" : "Удалить"}
                </Button>
              )}
            </Stack>
          </Stack>
          <Typography variant="body2">Тип: {item.instrumentTypeMeasurementType || "—"}</Typography>
          <Typography variant="body2">Наименование: {item.instrumentTypeName || "—"}</Typography>
          {item.modification && <Typography variant="body2">Модификация: {item.modification}</Typography>}
          <Typography variant="body2">Заводской номер: {item.serialNumber || "—"}</Typography>
          {item.registryNumber && <Typography variant="body2">Регистрационный номер: {item.registryNumber}</Typography>}
          <Stack direction="row" sx={{ flexWrap: "wrap", gap: 0.5 }}>
            {item.requestedOperations.map((operation) => (
              <Chip key={operation} label={OPERATION_LABELS[operation] ?? operation} size="small" />
            ))}
          </Stack>
          <Typography variant="body2">{item.comment || "—"}</Typography>
          {index < items.length - 1 && <Divider sx={{ pt: 1 }} />}
        </Stack>
      ))}

      <Dialog open={Boolean(editingItem)} onClose={closeEditor} fullWidth maxWidth="sm">
        <DialogTitle>Редактирование карточки СИ</DialogTitle>
        <DialogContent>
          <Stack spacing={2} sx={{ pt: 1 }}>
            {!editingItem?.instrumentId && (
              <TextField
                select
                label="Известное СИ"
                value={selectedInstrumentId}
                onChange={(event) => selectKnownDevice(event.target.value)}
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

            <TextField label="Тип СИ" value={editingItem?.instrumentTypeMeasurementType ?? ""} slotProps={{ input: { readOnly: true } }} fullWidth />
            <TextField label="Наименование СИ" value={editingItem?.instrumentTypeName ?? ""} slotProps={{ input: { readOnly: true } }} fullWidth />
            <TextField label="Модификация" value={modification} onChange={(event) => setModification(event.target.value)} fullWidth />
            <TextField label="Заводской номер" value={serialNumber} onChange={(event) => setSerialNumber(event.target.value)} required fullWidth />
            <TextField label="Регистрационный номер" value={registryNumber} onChange={(event) => setRegistryNumber(event.target.value)} fullWidth />
            <TextField label="Заводской номер изделия" value={factoryNumber} onChange={(event) => setFactoryNumber(event.target.value)} fullWidth />
            <TextField label="Год выпуска" type="number" value={manufactureYear} onChange={(event) => setManufactureYear(event.target.value)} fullWidth />
            <TextField label="Инвентарный номер" value={inventoryNumber} onChange={(event) => setInventoryNumber(event.target.value)} fullWidth />
            <TextField label="Комментарий" value={comment} onChange={(event) => setComment(event.target.value)} fullWidth multiline minRows={2} />

            {devicesQuery.isError && !editingItem?.instrumentId && (
              <Alert severity="warning">Не удалось загрузить список известных СИ. Можно создать новое СИ.</Alert>
            )}
            {(updateDeviceMutation.isError || createDeviceMutation.isError || assignMutation.isError) && (
              <Alert severity="error">Не удалось сохранить карточку СИ.</Alert>
            )}
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={closeEditor} disabled={isPending}>Отмена</Button>
          <Button variant="contained" onClick={saveDevice} disabled={(!selectedInstrumentId && !serialNumber.trim()) || !editingItem?.instrumentTypeId || isPending}>
            Сохранить
          </Button>
        </DialogActions>
      </Dialog>
    </Stack>
  );
}
