import { useEffect, useState } from "react";
import { Button, Stack, TextField, Typography } from "@mui/material";

import { useInstrumentType } from "../../instrument-type/model/useInstrumentType";
import { useUpdateDevice } from "../model/useUpdateDevice";
import type { DeviceRead, UpdateDeviceInput } from "../model/types";

interface DeviceCardProps {
  device: DeviceRead;
}

function toForm(device: DeviceRead): UpdateDeviceInput {
  return {
    serialNumber: device.serialNumber,
    registryNumber: device.registryNumber,
    modification: device.modification,
    factoryNumber: device.factoryNumber,
    manufactureYear: device.manufactureYear,
    inventoryNumber: device.inventoryNumber,
    comment: device.comment,
  };
}

export function DeviceCard({ device }: DeviceCardProps) {
  const { data: instrumentType } = useInstrumentType(device.instrumentTypeId);
  const updateMutation = useUpdateDevice(device.id);
  const [editing, setEditing] = useState(false);
  const [form, setForm] = useState<UpdateDeviceInput>(() => toForm(device));

  useEffect(() => {
    setForm(toForm(device));
  }, [device]);

  const setField = <K extends keyof UpdateDeviceInput>(
    field: K,
    value: UpdateDeviceInput[K],
  ) => setForm((current) => ({ ...current, [field]: value }));

  const save = () => {
    updateMutation.mutate(form, { onSuccess: () => setEditing(false) });
  };

  if (!editing) {
    return (
      <Stack spacing={1.5}>
        <Typography variant="h6">Карта СИ</Typography>
        <Typography>Наименование СИ: {instrumentType?.model ?? "—"}</Typography>
        <Typography>Тип СИ: {instrumentType?.name ?? "—"}</Typography>
        <Typography>Модификация: {device.modification ?? "—"}</Typography>
        <Typography>Серийный номер: {device.serialNumber}</Typography>
        <Typography>Регистрационный номер: {device.registryNumber ?? "—"}</Typography>
        <Typography>Заводской номер: {device.factoryNumber ?? "—"}</Typography>
        <Typography>Год выпуска: {device.manufactureYear ?? "—"}</Typography>
        <Typography>Инвентарный номер: {device.inventoryNumber ?? "—"}</Typography>
        <Typography>Комментарий: {device.comment ?? "—"}</Typography>
        <Button variant="outlined" onClick={() => setEditing(true)}>
          Редактировать карту СИ
        </Button>
      </Stack>
    );
  }

  return (
    <Stack spacing={1.5}>
      <Typography variant="h6">Карта СИ</Typography>
      <Typography>Наименование СИ: {instrumentType?.model ?? "—"}</Typography>
      <Typography>Тип СИ: {instrumentType?.name ?? "—"}</Typography>
      <TextField label="Модификация" value={form.modification ?? ""} onChange={(e) => setField("modification", e.target.value || null)} />
      <TextField label="Серийный номер" value={form.serialNumber} onChange={(e) => setField("serialNumber", e.target.value)} required />
      <TextField label="Регистрационный номер" value={form.registryNumber ?? ""} onChange={(e) => setField("registryNumber", e.target.value || null)} />
      <TextField label="Заводской номер" value={form.factoryNumber ?? ""} onChange={(e) => setField("factoryNumber", e.target.value || null)} />
      <TextField label="Год выпуска" type="number" value={form.manufactureYear ?? ""} onChange={(e) => setField("manufactureYear", e.target.value ? Number(e.target.value) : null)} />
      <TextField label="Инвентарный номер" value={form.inventoryNumber ?? ""} onChange={(e) => setField("inventoryNumber", e.target.value || null)} />
      <TextField label="Комментарий" multiline minRows={3} value={form.comment ?? ""} onChange={(e) => setField("comment", e.target.value || null)} />
      {updateMutation.error && <Typography color="error">Не удалось сохранить карту СИ.</Typography>}
      <Stack direction="row" spacing={1}>
        <Button variant="contained" disabled={!form.serialNumber.trim() || updateMutation.isPending} onClick={save}>
          Сохранить
        </Button>
        <Button disabled={updateMutation.isPending} onClick={() => { setForm(toForm(device)); setEditing(false); }}>
          Отмена
        </Button>
      </Stack>
    </Stack>
  );
}
