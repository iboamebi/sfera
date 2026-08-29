import { zodResolver } from "@hookform/resolvers/zod";
import { Button, MenuItem, Stack, TextField } from "@mui/material";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";

import { useCreateCustomer } from "../../../customers/model/useCreateCustomer";
import type { CreateCustomerSchema } from "../../../customers/model/schema";
import { CustomerForm } from "../../../customers/ui/CustomerForm";
import { useCustomers } from "../../../customers/model/useCustomers";
import { useOrders } from "../../model/useOrders";
import { createOrderSchema } from "../model/schema";
import type { CreateOrderForm as CreateOrderFormValues } from "../model/types";

interface CreateOrderFormProps {
  onSubmit: (data: CreateOrderFormValues) => void;
  isPending?: boolean;
}

function getLocalDateTimePlusDays(days: number): string {
  const date = new Date();
  date.setDate(date.getDate() + days);

  const pad = (value: number) => String(value).padStart(2, "0");

  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`;
}

function getNextOrderNumber(numbers: string[]): string {
  const numericNumbers = numbers
    .map((number) => Number(number))
    .filter((number) => Number.isInteger(number) && number >= 0);

  if (numericNumbers.length === 0) {
    return "1";
  }

  return String(Math.max(...numericNumbers) + 1);
}

export function CreateOrderForm({
  onSubmit,
  isPending = false,
}: CreateOrderFormProps) {
  const [isCreateCustomerOpen, setIsCreateCustomerOpen] = useState(false);
  const {
    register,
    handleSubmit,
    setValue,
    getValues,
    formState: { errors, dirtyFields },
  } = useForm<CreateOrderFormValues>({
    resolver: zodResolver(createOrderSchema),
    defaultValues: {
      plannedIssueAt: getLocalDateTimePlusDays(14),
    },
  });

  const {
    data: customers = [],
    isLoading: isCustomersLoading,
    isError: isCustomersError,
  } = useCustomers();
  const { data: orders = [], isLoading: isOrdersLoading } = useOrders();

  useEffect(() => {
    if (isOrdersLoading || dirtyFields.number || getValues("number")) {
      return;
    }

    setValue("number", getNextOrderNumber(orders.map((order) => order.number)), {
      shouldValidate: true,
    });
  }, [dirtyFields.number, getValues, isOrdersLoading, orders, setValue]);

  const createCustomerMutation = useCreateCustomer({
    onSuccess: (customer) => {
      setValue("customerId", customer.id, { shouldValidate: true });
      setIsCreateCustomerOpen(false);
    },
  });

  const handleCreateCustomer = (data: CreateCustomerSchema) => {
    createCustomerMutation.mutate(data);
  };

  if (isCreateCustomerOpen) {
    return (
      <Stack spacing={2}>
        <CustomerForm
          onSubmit={handleCreateCustomer}
          isPending={createCustomerMutation.isPending}
        />
        <Button
          onClick={() => setIsCreateCustomerOpen(false)}
          disabled={createCustomerMutation.isPending}
        >
          Вернуться к заказу
        </Button>
      </Stack>
    );
  }

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

        <Button
          onClick={() => setIsCreateCustomerOpen(true)}
          variant="outlined"
          disabled={isPending}
        >
          Создать клиента
        </Button>

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
