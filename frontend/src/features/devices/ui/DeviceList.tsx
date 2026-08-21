import { Stack, Typography } from "@mui/material";

import { useDevices } from "../model/useDevices";
import { DeviceListItem } from "./DeviceListItem";

export function DeviceList() {
  const { data: devices, isLoading, error } = useDevices();

  if (isLoading) {
    return <Typography>Loading devices...</Typography>;
  }

  if (error) {
    return <Typography>Не удалось загрузить средства измерений.</Typography>;
  }

  return (
    <Stack spacing={2}>
      {devices && devices.length === 0 && (
        <Typography>Средства измерений отсутствуют.</Typography>
      )}

      {devices?.map((device) => (
        <DeviceListItem key={device.id} device={device} />
      ))}
    </Stack>
  );
}
