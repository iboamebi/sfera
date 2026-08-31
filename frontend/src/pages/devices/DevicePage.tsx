import { Button, Stack, Typography } from "@mui/material";
import { useNavigate, useSearchParams, useParams } from "react-router";

import { DeviceCard } from "../../features/devices/ui/DeviceCard";
import { useDevice } from "../../features/devices/model/useDevice";

export function DevicePage() {
  const { deviceId } = useParams<{ deviceId: string }>();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { data, isLoading, error } = useDevice(deviceId ?? "");
  const returnToOrderId = searchParams.get("returnToOrder");

  const goBack = () => {
    if (returnToOrderId) {
      navigate(`/orders/${returnToOrderId}`);
      return;
    }
    navigate(-1);
  };

  if (isLoading) {
    return <Typography>Загрузка карты СИ...</Typography>;
  }

  if (error || !data) {
    return <Typography>Не удалось загрузить карту СИ.</Typography>;
  }

  return (
    <Stack spacing={2}>
      <Button variant="outlined" onClick={goBack} sx={{ alignSelf: "flex-start" }}>
        Назад
      </Button>
      <DeviceCard
        device={data}
        initialEditing={searchParams.get("edit") === "1"}
        onSaved={
          returnToOrderId
            ? () => navigate(`/orders/${returnToOrderId}`)
            : undefined
        }
      />
    </Stack>
  );
}
