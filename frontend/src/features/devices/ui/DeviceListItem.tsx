import { Stack, Typography } from "@mui/material";
import { Link } from "react-router";

import type { DeviceRead } from "../model/types";

interface DeviceListItemProps {
  device: DeviceRead;
}

export function DeviceListItem({ device }: DeviceListItemProps) {
  return (
    <Stack spacing={1}>
      <Typography>
        <Link to={`/devices/${device.id}`}>{device.serialNumber}</Link> — {device.status}
      </Typography>
    </Stack>
  );
}
