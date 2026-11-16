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
  const requestedReturnTo = searchParams.get("returnTo");
  const returnTo =
    requestedReturnTo &&
    (/^\/orders\/[^/?#]+$/.test(requestedReturnTo) ||
      /^\/customers\/[^/?#]+(?:\?returnTo=%2Forders%2F[^/?#]+)?$/i.test(requestedReturnTo) ||
      /^\/sites\/[^/?#]+(?:\?returnTo=%2Fcustomers%2F[^/?#]+(?:%3FreturnTo%3D%252Forders%252F[^/?#]+)?)?$/i.test(requestedReturnTo))
      ? requestedReturnTo
      : null;

  const goBack = () => {
    if (returnToOrderId) {
      navigate(`/orders/${returnToOrderId}`);
      return;
    }
    if (returnTo) {
      navigate(returnTo);
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
      <Button
        variant="outlined"
        onClick={goBack}
        sx={{ alignSelf: "flex-start" }}
      >
        {returnToOrderId || returnTo?.startsWith("/orders/")
          ? "Назад к заказу"
          : returnTo?.startsWith("/customers/")
            ? "Назад к клиенту"
            : returnTo?.startsWith("/sites/")
              ? "Назад к узлу"
              : "Назад"}
      </Button>
      <DeviceCard
        device={data}
        initialEditing={searchParams.get("edit") === "1"}
        onSaved={goBack}
        onCancel={goBack}
      />
    </Stack>
  );
}
