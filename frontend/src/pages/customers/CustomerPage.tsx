import { useMemo, useState } from "react";
import {
  Alert,
  Button,
  Divider,
  Stack,
  Typography,
} from "@mui/material";
import { Link, useNavigate, useParams, useSearchParams } from "react-router";

import { useCustomer } from "../../features/customers/model/useCustomer";
import { useUpdateCustomer } from "../../features/customers/model/useUpdateCustomer";
import { CustomerForm } from "../../features/customers/ui/CustomerForm";
import { useCustomerSites } from "../../features/sites/model/useCustomerSites";
import { useDevices } from "../../features/devices/model/useDevices";

export function CustomerPage() {
  const { customerId } = useParams<{ customerId: string }>();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const requestedReturnTo = searchParams.get("returnTo");
  const returnTo =
    requestedReturnTo && new RegExp("^/orders/[^/?#]+$").test(requestedReturnTo)
      ? requestedReturnTo
      : "/customers";
  const [isEditing, setIsEditing] = useState(false);
  const { data, error, isLoading } = useCustomer(customerId ?? "");
  const {
    data: sites,
    error: sitesError,
    isLoading: sitesLoading,
  } = useCustomerSites(customerId ?? "");
  const {
    data: allDevices,
    error: devicesError,
    isLoading: devicesLoading,
  } = useDevices();
  const updateMutation = useUpdateCustomer(customerId ?? "", {
    onSuccess: () => setIsEditing(false),
  });

  const customerDevices = useMemo(
    () => (allDevices ?? [])
      .filter((device) => device.customerId === customerId)
      .sort((left, right) =>
        (left.name ?? left.serialNumber).localeCompare(
          right.name ?? right.serialNumber,
          "ru",
          { numeric: true },
        ),
      ),
    [allDevices, customerId],
  );

  const devicesBySite = useMemo(() => {
    const groups = new Map<string, typeof customerDevices>();
    for (const device of customerDevices) {
      if (!device.siteId) continue;
      const group = groups.get(device.siteId) ?? [];
      group.push(device);
      groups.set(device.siteId, group);
    }
    return groups;
  }, [customerDevices]);

  const unassignedDevices = customerDevices.filter((device) => !device.siteId);

  if (isLoading) {
    return <Typography>Загрузка клиента...</Typography>;
  }

  if (error) {
    return <Typography>Не удалось загрузить клиента.</Typography>;
  }

  if (!data) {
    return null;
  }

  return (
    <Stack spacing={3}>
      <Button
        variant="outlined"
        onClick={() => navigate(returnTo)}
        sx={{ alignSelf: "flex-start" }}
      >
        {returnTo.startsWith("/orders/") ? "Назад к заказу" : "Назад к клиентам"}
      </Button>

      {isEditing ? (
        <Stack spacing={2} sx={{ maxWidth: 720 }}>
          <Typography variant="h5">Редактирование клиента</Typography>

          {updateMutation.isError && (
            <Alert severity="error">
              Не удалось сохранить данные клиента. Проверьте данные и
              повторите попытку.
            </Alert>
          )}

          <CustomerForm
            initialValues={{
              name: data.name,
              contactPerson: data.contactPerson ?? "",
              phone: data.phone ?? "",
              email: data.email ?? "",
              comment: data.comment ?? "",
              discountPercent: data.discountPercent,
            }}
            submitLabel="Сохранить изменения"
            onSubmit={(formData) => updateMutation.mutate(formData)}
            isPending={updateMutation.isPending}
          />

          <Button
            disabled={updateMutation.isPending}
            onClick={() => setIsEditing(false)}
            sx={{ alignSelf: "flex-start" }}
          >
            Отмена
          </Button>
        </Stack>
      ) : (
        <>
          <Stack spacing={2}>
            <Typography variant="h5">{data.name}</Typography>

            {data.contactPerson && (
              <Typography color="text.secondary">
                Контактное лицо: {data.contactPerson}
              </Typography>
            )}

            {data.phone && <Typography>Телефон: {data.phone}</Typography>}
            {data.email && <Typography>E-mail: {data.email}</Typography>}
            {data.comment && <Typography>{data.comment}</Typography>}

            <Typography>Скидка: {data.discountPercent}%</Typography>

            {data.archived && (
              <Typography color="text.secondary">В архиве</Typography>
            )}

            {!data.archived && (
              <Button
                variant="contained"
                onClick={() => setIsEditing(true)}
                sx={{ alignSelf: "flex-start" }}
              >
                Редактировать
              </Button>
            )}
          </Stack>

          <Divider />

          <Stack spacing={2}>
            <Stack
              direction="row"
              spacing={2}
              sx={{
                alignItems: { xs: "stretch", sm: "center" },
                justifyContent: "space-between",
                flexWrap: "wrap",
              }}
            >
              <Typography variant="h6">
                Узлы ({sites?.length ?? 0})
              </Typography>
              {!data.archived && (
                <Button
                  component={Link}
                  to={`/customers/${data.id}/sites/new`}
                  variant="outlined"
                >
                  Добавить узел
                </Button>
              )}
            </Stack>

            {sitesLoading && <Typography>Загрузка узлов...</Typography>}
            {sitesError && (
              <Alert severity="error">Не удалось загрузить узлы.</Alert>
            )}
            {!sitesLoading && !sitesError && (!sites || sites.length === 0) && (
              <Typography color="text.secondary">
                Узлы пока не зарегистрированы.
              </Typography>
            )}

            {!sitesLoading && !sitesError && sites && sites.length > 0 && (
              <Stack spacing={2}>
                {sites.map((site) => {
                  const siteDevices = devicesBySite.get(site.id) ?? [];
                  return (
                    <Stack key={site.id} spacing={1}>
                      <Stack
                        direction="row"
                        spacing={1}
                        sx={{ alignItems: "baseline", flexWrap: "wrap" }}
                      >
                        <Typography variant="subtitle1">{site.name}</Typography>
                        {site.archived && (
                          <Typography color="text.secondary" variant="caption">
                            В архиве
                          </Typography>
                        )}
                      </Stack>
                      <Typography color="text.secondary">{site.address}</Typography>
                      {devicesError ? null : siteDevices.length === 0 ? (
                        <Typography color="text.secondary" variant="body2">
                          Известные СИ не привязаны.
                        </Typography>
                      ) : (
                        <Stack spacing={0.75} sx={{ pl: 1 }}>
                          {siteDevices.map((device) => (
                            <Typography key={device.id} variant="body2">
                              <Link to={`/devices/${device.id}`}>
                                {device.name ?? "Без наименования"}
                              </Link>
                              {" · Зав. № "}
                              {device.serialNumber}
                            </Typography>
                          ))}
                        </Stack>
                      )}
                    </Stack>
                  );
                })}
              </Stack>
            )}
          </Stack>

          <Divider />

          <Stack spacing={2}>
            <Stack
              direction="row"
              spacing={2}
              sx={{
                alignItems: { xs: "stretch", sm: "center" },
                justifyContent: "space-between",
                flexWrap: "wrap",
              }}
            >
              <Typography variant="h6">
                СИ без привязки к узлу ({unassignedDevices.length})
              </Typography>
              {!data.archived && (
                <Button
                  component={Link}
                  to={`/customers/${data.id}/devices/new`}
                  variant="contained"
                >
                  Добавить СИ
                </Button>
              )}
            </Stack>

            {devicesLoading && <Typography>Загрузка СИ...</Typography>}
            {devicesError && (
              <Alert severity="error">Не удалось загрузить список СИ.</Alert>
            )}
            {!devicesLoading && !devicesError && unassignedDevices.length === 0 && (
              <Typography color="text.secondary">
                Нет известных СИ без привязки к узлу.
              </Typography>
            )}
            {!devicesLoading && !devicesError && unassignedDevices.length > 0 && (
              <Stack spacing={0.75}>
                {unassignedDevices.map((device) => (
                  <Typography key={device.id} variant="body2">
                    <Link to={`/devices/${device.id}`}>
                      {device.name ?? "Без наименования"}
                    </Link>
                    {" · Зав. № "}
                    {device.serialNumber}
                  </Typography>
                ))}
              </Stack>
            )}
          </Stack>

          <Typography color="text.secondary" variant="caption">
            Отображаются только сведения, зарегистрированные в Sfera. Список СИ
            не обязательно отражает полный состав оборудования клиента или узла.
          </Typography>
        </>
      )}
    </Stack>
  );
}
