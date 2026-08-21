import { MenuItem, TextField, Typography } from "@mui/material";

import { useDevices } from "../../../devices/model/useDevices";

interface DeviceSelectorProps {
  value: string;
  onChange: (deviceId: string) => void;
}

export function DeviceSelector({ value, onChange }: DeviceSelectorProps) {
  const { data: devices, isLoading, error } = useDevices();

  if (error) {
    return (
      <Typography color="error">
        Не удалось загрузить средства измерений.
      </Typography>
    );
  }

  if (!isLoading && devices?.length === 0) {
    return (
      <Typography>
        Средства измерений отсутствуют. Создайте средство измерений, чтобы
        добавить его в заказ.
      </Typography>
    );
  }

  return (
    <TextField
      select
      fullWidth
      label="Средство измерений"
      value={value}
      onChange={(event) => onChange(event.target.value)}
      disabled={isLoading}
    >
      {devices?.map((device) => (
        <MenuItem key={device.id} value={device.id}>
          {device.serialNumber}
        </MenuItem>
      ))}
    </TextField>
  );
}
