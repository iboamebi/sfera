import { Stack, Typography } from "@mui/material";
import { useSearchParams, useParams } from "react-router";

import { DeviceCard } from "../../features/devices/ui/DeviceCard";
import { useDevice } from "../../features/devices/model/useDevice";

export function DevicePage() {
  const { deviceId } = useParams<{ deviceId: string }>();
  const [searchParams] = useSearchParams();
  const { data, isLoading, error } = useDevice(deviceId ?? "");

  if (isLoading) {
    return <Typography>Загрузка карты СИ...</Typography>;
  }

  if (error || !data) {
    return <Typography>Не удалось загрузить карту СИ.</Typography>;
  }

  return (
    <Stack spacing={2}>
      <DeviceCard
        device={data}
        initialEditing={searchParams.get("edit") === "1"}
      />
    </Stack>
  );
}
