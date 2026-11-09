import { useQueryClient } from "@tanstack/react-query";
import { Alert, Button, Stack, Typography } from "@mui/material";
import { useNavigate, useParams } from "react-router";

import { useCreateSite } from "../../features/sites/model/useCreateSite";
import { SiteForm } from "../../features/sites/ui/SiteForm";

export function CreateSitePage() {
  const { customerId } = useParams<{ customerId: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const mutation = useCreateSite({
    onSuccess: async (site) => {
      await queryClient.invalidateQueries({
        queryKey: ["sites", "customer", customerId],
      });
      navigate(`/customers/${site.customerId}`);
    },
  });

  if (!customerId) {
    return <Typography>Клиент не указан.</Typography>;
  }

  return (
    <Stack spacing={3} sx={{ maxWidth: 720 }}>
      <Button
        variant="outlined"
        onClick={() => navigate(`/customers/${customerId}`)}
        sx={{ alignSelf: "flex-start" }}
      >
        Назад к клиенту
      </Button>

      <Typography variant="h4">Создание объекта</Typography>

      {mutation.isError && (
        <Alert severity="error">
          Не удалось создать объект. Проверьте данные и повторите попытку.
        </Alert>
      )}

      <SiteForm
        onSubmit={(data) => mutation.mutate({ ...data, customerId })}
        isPending={mutation.isPending}
      />
    </Stack>
  );
}
