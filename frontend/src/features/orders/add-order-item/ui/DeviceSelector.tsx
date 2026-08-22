import { Button, MenuItem, Stack, TextField, Typography } from "@mui/material";

import { useDevices } from "../../../devices/model/useDevices";

interface DeviceSelectorProps {
  value: string;
  onChange: (deviceId: string) => void;
  onCreateDevice?: () => void;
}

export function DeviceSelector({
  value,
  onChange,
  onCreateDevice,
}: DeviceSelectorProps) {
  const { data: devices, isLoading, error } = useDevices();

  if (error) {
    return (
      <Typography color="error">
        Не удалось загрузить средства измерений.
      </Typography>
    );
  }

  return (
    <Stack spacing={1}>
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

      {onCreateDevice && (
        <Button
          onClick={onCreateDevice}
          variant="outlined"
          disabled={isLoading}
        >
          Создать СИ
        </Button>
      )}
    </Stack>
  );
}
