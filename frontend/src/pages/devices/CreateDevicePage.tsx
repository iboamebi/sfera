import { useState } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { Alert, Button, MenuItem, Stack, TextField, Typography } from "@mui/material";
import { useNavigate } from "react-router";

import { useCustomers } from "../../features/customers/model/useCustomers";
import { useCreateDevice } from "../../features/devices/model/useCreateDevice";
import { DeviceForm } from "../../features/devices/ui/DeviceForm";

export function CreateDevicePage() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [customerId, setCustomerId] = useState("");
  const { data: customers = [], isLoading, isError } = useCustomers();

  const mutation = useCreateDevice({
    onSuccess: async (device) => {
      await queryClient.invalidateQueries({ queryKey: ["devices"] });
      navigate(`/devices/${device.id}`);
    },
  });

  const activeCustomers = customers.filter((customer) => !customer.archived);

  return (
    <Stack spacing={3} sx={{ maxWidth: 720 }}>
      <Button
        variant="outlined"
        onClick={() => navigate("/devices")}
        sx={{ alignSelf: "flex-start" }}
      >
        Назад к СИ
      </Button>

      <Typography variant="h4">Создание СИ</Typography>

      {isError && (
        <Alert severity="error">
          Не удалось загрузить список клиентов.
        </Alert>
      )}

      <TextField
        select
        label="Клиент"
        value={customerId}
        onChange={(event) => setCustomerId(event.target.value)}
        disabled={isLoading || isError || mutation.isPending}
        helperText={isLoading ? "Загрузка клиентов..." : "Выберите владельца средства измерений"}
      >
        {activeCustomers.map((customer) => (
          <MenuItem key={customer.id} value={customer.id}>
            {customer.name}
          </MenuItem>
        ))}
      </TextField>

      {mutation.isError && (
        <Alert severity="error">
          Не удалось создать СИ. Проверьте данные и повторите попытку.
        </Alert>
      )}

      {customerId && (
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
      )}
    </Stack>
  );
}
