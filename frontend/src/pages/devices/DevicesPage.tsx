import { Button, Stack, Typography } from "@mui/material";
import { Link } from "react-router";

import { DeviceList } from "../../features/devices/ui/DeviceList";

export function DevicesPage() {
  return (
    <Stack spacing={2}>
      <Stack direction="row" spacing={2} sx={{ alignItems: "center", justifyContent: "space-between" }}>
        <Typography variant="h5">Средства измерений</Typography>
        <Button component={Link} to="/devices/new" variant="contained">
          Создать СИ
        </Button>
      </Stack>
      <DeviceList />
    </Stack>
  );
}
