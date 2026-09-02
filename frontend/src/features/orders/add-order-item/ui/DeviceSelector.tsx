import { Autocomplete, Button, Stack, TextField, Typography } from "@mui/material";

import type { DeviceRead } from "../../../devices/model/types";
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
  const { data: devices = [], isLoading, error } = useDevices();
  const selectedDevice =
    devices.find((device) => device.id === value) ?? null;

  if (error) {
    return (
      <Typography color="error">
        Не удалось загрузить средства измерений.
      </Typography>
    );
  }

  return (
    <Stack spacing={1} sx={{ width: "100%" }}>
      <Autocomplete
        fullWidth
        options={devices}
        value={selectedDevice}
        loading={isLoading}
        getOptionLabel={(device) => device.serialNumber}
        isOptionEqualToValue={(option, selected) => option.id === selected.id}
        onChange={(_, device: DeviceRead | null) =>
          onChange(device?.id ?? "")
        }
        renderInput={(params) => (
          <TextField
            {...params}
            fullWidth
            label="Средство измерений"
            placeholder="Введите серийный номер"
          />
        )}
      />

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
