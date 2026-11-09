import { useQueryClient } from "@tanstack/react-query";
import { Alert, Button, Stack, Typography } from "@mui/material";
import { useNavigate } from "react-router";

import { useCreateOrganization } from "../../features/organizations/model/useCreateOrganization";
import { OrganizationForm } from "../../features/organizations/ui/OrganizationForm";

export function CreateOrganizationPage() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const mutation = useCreateOrganization({
    onSuccess: async (organization) => {
      await queryClient.invalidateQueries({ queryKey: ["organizations"] });
      navigate(`/organizations/${organization.id}`);
    },
  });

  return (
    <Stack spacing={3} sx={{ maxWidth: 720 }}>
      <Button
        variant="outlined"
        onClick={() => navigate("/organizations")}
        sx={{ alignSelf: "flex-start" }}
      >
        Назад к организациям
      </Button>

      <Typography variant="h4">Создание организации</Typography>

      {mutation.isError && (
        <Alert severity="error">
          Не удалось создать организацию. Проверьте данные и повторите попытку.
        </Alert>
      )}

      <OrganizationForm
        onSubmit={(data) => mutation.mutate(data)}
        isPending={mutation.isPending}
      />
    </Stack>
  );
}
