import { zodResolver } from "@hookform/resolvers/zod";
import { Button, MenuItem, Stack, TextField } from "@mui/material";
import { useForm } from "react-hook-form";

import { useCustomers } from "../../../customers/model/useCustomers";
import { createOrderSchema } from "../model/schema";
import type { CreateOrderForm as CreateOrderFormValues } from "../model/types";

interface CreateOrderFormProps {
  onSubmit: (data: CreateOrderFormValues) => void;
  isPending?: boolean;
}

export function CreateOrderForm({
  onSubmit,
  isPending = false,
}: CreateOrderFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<CreateOrderFormValues>({
    resolver: zodResolver(createOrderSchema),
  });

  const {
    data: customers = [],
    isLoading: isCustomersLoading,
    isError: isCustomersError,
  } = useCustomers();

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Stack spacing={2}>
        <TextField
          label="Номер заказа"
          {...register("number")}
          error={Boolean(errors.number)}
          helperText={errors.number?.message}
          disabled={isPending}
        />

        <TextField
          select
          label="Клиент"
          {...register("customerId")}
          error={Boolean(errors.customerId)}
          helperText={
            errors.customerId?.message ??
            (isCustomersError ? "Не удалось загрузить клиентов" : undefined)
          }
          disabled={isPending || isCustomersLoading || isCustomersError}
        >
          {customers
            .filter((customer) => !customer.archived)
            .map((customer) => (
              <MenuItem key={customer.id} value={customer.id}>
                {customer.name}
              </MenuItem>
            ))}
        </TextField>

        <TextField
          label="Планируемая дата выдачи"
          type="datetime-local"
          {...register("plannedIssueAt")}
          error={Boolean(errors.plannedIssueAt)}
          helperText={errors.plannedIssueAt?.message}
          disabled={isPending}
          slotProps={{
            inputLabel: {
              shrink: true,
            },
          }}
        />

        <TextField
          label="Комментарий"
          multiline
          minRows={3}
          {...register("comment")}
          error={Boolean(errors.comment)}
          helperText={errors.comment?.message}
          disabled={isPending}
        />

        <Button
          type="submit"
          variant="contained"
          disabled={isPending || isCustomersLoading || isCustomersError}
        >
          {isPending ? "Создание..." : "Создать заказ"}
        </Button>
      </Stack>
    </form>
  );
}
