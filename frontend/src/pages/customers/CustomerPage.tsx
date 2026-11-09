import { useState } from "react";
import { Alert, Button, Stack, Typography } from "@mui/material";
import { Link, useNavigate, useParams } from "react-router";

import { useCustomer } from "../../features/customers/model/useCustomer";
import { useUpdateCustomer } from "../../features/customers/model/useUpdateCustomer";
import { CustomerForm } from "../../features/customers/ui/CustomerForm";
import { useCustomerSites } from "../../features/sites/model/useCustomerSites";

export function CustomerPage() {
  const { customerId } = useParams<{ customerId: string }>();
  const navigate = useNavigate();
  const [isEditing, setIsEditing] = useState(false);
  const { data, error, isLoading } = useCustomer(customerId ?? "");
  const {
    data: sites,
    error: sitesError,
    isLoading: sitesLoading,
  } = useCustomerSites(customerId ?? "");
  const updateMutation = useUpdateCustomer(customerId ?? "", {
    onSuccess: () => setIsEditing(false),
  });

  if (isLoading) {
    return <Typography>Loading...</Typography>;
  }

  if (error) {
    return <Typography>Failed to load customer.</Typography>;
  }

  if (!data) {
    return null;
  }

  return (
    <Stack spacing={3}>
      <Button
        variant="outlined"
        onClick={() => navigate("/customers")}
        sx={{ alignSelf: "flex-start" }}
      >
        Назад к клиентам
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
                {data.contactPerson}
              </Typography>
            )}

            {data.phone && <Typography>{data.phone}</Typography>}
            {data.email && <Typography>{data.email}</Typography>}
            {data.comment && <Typography>{data.comment}</Typography>}

            <Typography>Discount: {data.discountPercent}%</Typography>

            {data.archived && (
              <Typography color="text.secondary">Archived</Typography>
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
              <Typography variant="h6">Объекты</Typography>
              <Stack direction="row" spacing={1}>
                <Button
                  component={Link}
                  to={`/customers/${data.id}/devices/new`}
                  variant="contained"
                >
                  Добавить СИ
                </Button>
                <Button
                  component={Link}
                  to={`/customers/${data.id}/sites/new`}
                  variant="outlined"
                >
                  Добавить объект
                </Button>
              </Stack>
            </Stack>

            {sitesLoading && <Typography>Загрузка объектов...</Typography>}

            {sitesError && (
              <Typography>Не удалось загрузить объекты.</Typography>
            )}

            {!sitesLoading && !sitesError && (!sites || sites.length === 0) && (
              <Typography color="text.secondary">
                Объекты пока не созданы.
              </Typography>
            )}

            {!sitesLoading && !sitesError && sites && sites.length > 0 && (
              <Stack spacing={1.5}>
                {sites.map((site) => (
                  <Stack key={site.id} spacing={0.5}>
                    <Typography variant="subtitle1">{site.name}</Typography>
                    <Typography color="text.secondary">
                      {site.address}
                    </Typography>
                    {site.archived && (
                      <Typography color="text.secondary">В архиве</Typography>
                    )}
                  </Stack>
                ))}
              </Stack>
            )}
          </Stack>
        </>
      )}
    </Stack>
  );
}
