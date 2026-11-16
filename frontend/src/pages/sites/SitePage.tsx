import { useMemo } from "react";
import { Alert, Button, Divider, Stack, Typography } from "@mui/material";
import { Link, useNavigate, useParams, useSearchParams } from "react-router";

import { useCustomer } from "../../features/customers/model/useCustomer";
import { useDevices } from "../../features/devices/model/useDevices";
import { useSite } from "../../features/sites/model/useSite";

export function SitePage() {
  const { siteId } = useParams<{ siteId: string }>();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const requestedReturnTo = searchParams.get("returnTo");
  const returnTo =
    requestedReturnTo &&
    (/^\/customers\/[^/?#]+$/.test(requestedReturnTo) ||
      /^\/customers\/[^/?#]+\?returnTo=%2Forders%2F[^/?#]+$/i.test(requestedReturnTo))
      ? requestedReturnTo
      : "/sites";
  const deviceReturnTo = "/sites/" + siteId + "?returnTo=" + encodeURIComponent(returnTo);

  const {
    data: site,
    error: siteError,
    isLoading: siteLoading,
  } = useSite(siteId ?? "");
  const {
    data: customer,
    error: customerError,
    isLoading: customerLoading,
  } = useCustomer(site?.customerId ?? "");
  const {
    data: allDevices,
    error: devicesError,
    isLoading: devicesLoading,
  } = useDevices();

  const siteDevices = useMemo(
    () =>
      (allDevices ?? [])
        .filter((device) => device.siteId === siteId)
        .sort((left, right) =>
          (left.name ?? left.serialNumber).localeCompare(
            right.name ?? right.serialNumber,
            "ru",
            { numeric: true },
          ),
        ),
    [allDevices, siteId],
  );

  if (siteLoading) {
    return <Typography>Загрузка узла...</Typography>;
  }

  if (siteError || !site) {
    return <Typography color="error">Не удалось загрузить узел.</Typography>;
  }

  return (
    <Stack spacing={3}>
      <Button
        variant="outlined"
        onClick={() => navigate(returnTo)}
        sx={{ alignSelf: "flex-start" }}
      >
        {returnTo.startsWith("/customers/")
          ? "Назад к клиенту"
          : "Назад к узлам"}
      </Button>

      <Stack spacing={1}>
        <Typography variant="h5">{site.name}</Typography>
        <Typography color="text.secondary">{site.address}</Typography>
        {site.archived && (
          <Typography color="text.secondary">Узел в архиве</Typography>
        )}
      </Stack>

      <Divider />

      <Stack spacing={1}>
        <Typography variant="h6">Клиент</Typography>
        {customerLoading ? (
          <Typography color="text.secondary">Загрузка клиента...</Typography>
        ) : customerError || !customer ? (
          <Alert severity="error">Не удалось загрузить данные клиента.</Alert>
        ) : (
          <Typography>{customer.name}</Typography>
        )}
      </Stack>

      <Divider />

      <Stack spacing={2}>
        <Typography variant="h6">
          Зарегистрированные СИ
          {!devicesLoading && !devicesError && " (" + siteDevices.length + ")"}
        </Typography>

        {devicesLoading && (
          <Typography color="text.secondary">Загрузка СИ...</Typography>
        )}
        {devicesError && (
          <Alert severity="error">Не удалось загрузить список СИ.</Alert>
        )}
        {!devicesLoading && !devicesError && siteDevices.length === 0 && (
          <Typography color="text.secondary">
            В Sfera пока нет зарегистрированных СИ, привязанных к этому узлу.
          </Typography>
        )}
        {!devicesLoading && !devicesError && siteDevices.length > 0 && (
          <Stack spacing={1}>
            {siteDevices.map((device) => (
              <Typography key={device.id} variant="body2">
                <Link
                  to={"/devices/" + device.id + "?returnTo=" + encodeURIComponent(deviceReturnTo)}
                >
                  {device.name ?? "Без наименования"}
                </Link>
                {" · Зав. № "}
                {device.serialNumber}
                {device.registryNumber && " · Госреестр № " + device.registryNumber}
              </Typography>
            ))}
          </Stack>
        )}
      </Stack>

      <Typography color="text.secondary" variant="caption">
        Отображаются только сведения, зарегистрированные в Sfera. Список СИ
        не обязательно отражает полный физический состав узла.
      </Typography>
    </Stack>
  );
}
