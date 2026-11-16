import { useState } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { Alert, Button, MenuItem, Stack, TextField, Typography } from "@mui/material";
import { useNavigate } from "react-router";

import { useCustomers } from "../../features/customers/model/useCustomers";
import { useCreateSite } from "../../features/sites/model/useCreateSite";
import { SiteForm } from "../../features/sites/ui/SiteForm";

export function CreateSiteDirectoryPage() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { data: customers, isLoading: customersLoading, error: customersError } = useCustomers();
  const [customerId, setCustomerId] = useState("");
  const mutation = useCreateSite({
    onSuccess: async () => {
      await Promise.all([
        queryClient.invalidateQueries({ queryKey: ["sites"] }),
        queryClient.invalidateQueries({ queryKey: ["sites", "customer"] }),
      ]);
      navigate("/sites");
    },
  });

  const activeCustomers = (customers ?? []).filter((customer) => !customer.archived);

  return (
    <Stack spacing={3} sx={{ maxWidth: 720 }}>
      <Button
        variant="outlined"
        onClick={() => navigate("/sites")}
        sx={{ alignSelf: "flex-start" }}
      >
        Назад к узлам
      </Button>

      <Typography variant="h4">Создание узла</Typography>

      {customersLoading && <Typography>Загрузка клиентов...</Typography>}
      {customersError && (
        <Alert severity="error">Не удалось загрузить список клиентов.</Alert>
      )}

      {!customersLoading && !customersError && (
        <>
          {activeCustomers.length === 0 ? (
            <Alert severity="warning">
              Нет активных клиентов. Сначала создайте клиента.
            </Alert>
          ) : (
            <>
              <TextField
                select
                label="Клиент"
                value={customerId}
                onChange={(event) => setCustomerId(event.target.value)}
                required
                fullWidth
              >
                {activeCustomers.map((customer) => (
                  <MenuItem key={customer.id} value={customer.id}>
                    {customer.name}
                  </MenuItem>
                ))}
              </TextField>

              {mutation.isError && (
                <Alert severity="error">
                  Не удалось создать узел. Проверьте данные и повторите попытку.
                </Alert>
              )}

              {customerId ? (
                <SiteForm
                  onSubmit={(data) => mutation.mutate({ ...data, customerId })}
                  isPending={mutation.isPending}
                />
              ) : (
                <Typography color="text.secondary">
                  Выберите клиента, чтобы заполнить данные узла.
                </Typography>
              )}
            </>
          )}
        </>
      )}
    </Stack>
  );
}
