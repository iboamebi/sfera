import { Stack, Typography } from "@mui/material";

import type { DeviceRead } from "../model/types";

interface DeviceListItemProps {
  device: DeviceRead;
}

export function DeviceListItem({ device }: DeviceListItemProps) {
  return (
    <Stack spacing={1}>
      <Typography>
        {device.serialNumber} — {device.status}
      </Typography>
    </Stack>
  );
}
