import { useQueryClient } from "@tanstack/react-query";
import { Alert, Button, Stack, Typography } from "@mui/material";
import { useNavigate, useParams } from "react-router";

import { useCreateDevice } from "../../features/devices/model/useCreateDevice";
import { DeviceForm } from "../../features/devices/ui/DeviceForm";

export function CreateDevicePage() {
  const { customerId } = useParams<{ customerId: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const mutation = useCreateDevice({
    onSuccess: async (device) => {
      await queryClient.invalidateQueries({ queryKey: ["devices"] });
      navigate(`/devices/${device.id}`);
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

      <Typography variant="h4">Создание СИ</Typography>

      {mutation.isError && (
        <Alert severity="error">
          Не удалось создать СИ. Проверьте данные и повторите попытку.
        </Alert>
      )}

      <DeviceForm
        customerId={customerId}
        onSubmit={(data) =>
          mutation.mutate({
            ...data,
            customerId,
          })
        }
        isPending={mutation.isPending}
      />
    </Stack>
  );
}
