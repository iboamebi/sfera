import { Stack, Typography } from "@mui/material";

import { DeviceList } from "../../features/devices/ui/DeviceList";

export function DevicesPage() {
  return (
    <Stack spacing={2}>
      <Typography variant="h5">Средства измерений</Typography>
      <DeviceList />
    </Stack>
  );
}
