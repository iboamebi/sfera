import { useQueryClient } from "@tanstack/react-query";
import { Alert, Button, Stack, Typography } from "@mui/material";
import { useNavigate } from "react-router";

import { useCreateCustomer } from "../../features/customers/model/useCreateCustomer";
import { CustomerForm } from "../../features/customers/ui/CustomerForm";

export function CreateCustomerPage() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const mutation = useCreateCustomer({
    onSuccess: async (customer) => {
      await queryClient.invalidateQueries({ queryKey: ["customers"] });
      navigate(`/customers/${customer.id}`);
    },
  });

  return (
    <Stack spacing={3} sx={{ maxWidth: 720 }}>
      <Button
        variant="outlined"
        onClick={() => navigate("/customers")}
        sx={{ alignSelf: "flex-start" }}
      >
        Назад к клиентам
      </Button>

      <Typography variant="h4">Создание клиента</Typography>

      {mutation.isError && (
        <Alert severity="error">
          Не удалось создать клиента. Проверьте данные и повторите попытку.
        </Alert>
      )}

      <CustomerForm
        onSubmit={(data) => mutation.mutate(data)}
        isPending={mutation.isPending}
      />
    </Stack>
  );
}
