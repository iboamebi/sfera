import { useState } from "react";
import { Alert, Button, Stack, Typography } from "@mui/material";
import { useNavigate, useParams } from "react-router";

import { useOrganization } from "../../features/organizations/model/useOrganization";
import { useUpdateOrganization } from "../../features/organizations/model/useUpdateOrganization";
import { OrganizationForm } from "../../features/organizations/ui/OrganizationForm";

export function OrganizationPage() {
  const { organizationId } = useParams<{ organizationId: string }>();
  const navigate = useNavigate();
  const [isEditing, setIsEditing] = useState(false);
  const { data, error, isLoading } = useOrganization(organizationId ?? "");
  const updateMutation = useUpdateOrganization(organizationId ?? "", {
    onSuccess: () => setIsEditing(false),
  });

  if (isLoading) {
    return <Typography>Загрузка организации...</Typography>;
  }

  if (error) {
    return <Typography>Не удалось загрузить организацию.</Typography>;
  }

  if (!data) {
    return null;
  }

  return (
    <Stack spacing={2} sx={{ maxWidth: 720 }}>
      <Button
        variant="outlined"
        onClick={() => navigate("/organizations")}
        sx={{ alignSelf: "flex-start" }}
      >
        Назад к организациям
      </Button>

      {isEditing ? (
        <>
          <Typography variant="h5">Редактирование организации</Typography>
          {updateMutation.isError && (
            <Alert severity="error">
              Не удалось сохранить реквизиты организации. Проверьте данные и
              повторите попытку.
            </Alert>
          )}
          <OrganizationForm
            initialValues={{
              name: data.name,
              shortName: data.shortName ?? "",
              inn: data.inn ?? "",
              kpp: data.kpp ?? "",
              ogrn: data.ogrn ?? "",
              address: data.address ?? "",
              phone: data.phone ?? "",
              email: data.email ?? "",
              website: data.website ?? "",
              comment: data.comment ?? "",
            }}
            submitLabel="Сохранить изменения"
            onSubmit={(formData) => updateMutation.mutate(formData)}
            isPending={updateMutation.isPending}
          />
          <Button
            disabled={updateMutation.isPending}
            onClick={() => setIsEditing(false)}
          >
            Отмена
          </Button>
        </>
      ) : (
        <>
          <Typography variant="h5">{data.name}</Typography>
          {data.shortName && (
            <Typography color="text.secondary">{data.shortName}</Typography>
          )}
          {data.inn && <Typography>ИНН: {data.inn}</Typography>}
          {data.kpp && <Typography>КПП: {data.kpp}</Typography>}
          {data.ogrn && <Typography>ОГРН: {data.ogrn}</Typography>}
          {data.address && <Typography>{data.address}</Typography>}
          {data.phone && <Typography>{data.phone}</Typography>}
          {data.email && <Typography>{data.email}</Typography>}
          {data.website && <Typography>{data.website}</Typography>}
          {data.comment && <Typography>{data.comment}</Typography>}
          <Button
            variant="contained"
            onClick={() => setIsEditing(true)}
            sx={{ alignSelf: "flex-start" }}
          >
            Редактировать реквизиты
          </Button>
        </>
      )}
    </Stack>
  );
}
