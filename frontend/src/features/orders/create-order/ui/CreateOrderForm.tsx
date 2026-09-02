import { zodResolver } from "@hookform/resolvers/zod";
import { Button, MenuItem, Stack, TextField } from "@mui/material";
import { useEffect, useRef, useState } from "react";
import { useForm } from "react-hook-form";

import { useCreateCustomer } from "../../../customers/model/useCreateCustomer";
import { useQueryClient } from "@tanstack/react-query";
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

function getDefaultPlannedIssueAt(): string {
  const date = new Date();
  date.setDate(date.getDate() + 14);

  const pad = (value: number) => String(value).padStart(2, "0");

  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`;
}

function getNextOrderNumber(numbers: string[]): string {
  const usedNumbers = new Set(
    numbers
      .map((number) => Number(number.trim()))
      .filter((number) => Number.isInteger(number) && number > 0),
  );

  let nextNumber = 1;
  while (usedNumbers.has(nextNumber)) {
    nextNumber += 1;
  }

  return String(nextNumber);
}

export function CreateOrderForm({
  onSubmit,
  isPending = false,
}: CreateOrderFormProps) {
  const queryClient = useQueryClient();
  const [isCreateCustomerOpen, setIsCreateCustomerOpen] = useState(false);
  const customerSelectRef = useRef<HTMLInputElement | null>(null);
  const {
    register,
    handleSubmit,
    setValue,
    getValues,
    formState: { errors },
  } = useForm<CreateOrderFormValues>({
    resolver: zodResolver(createOrderSchema),
    defaultValues: {
      plannedIssueAt: getDefaultPlannedIssueAt(),
    },
  });

  const {
    data: customers = [],
    isLoading: isCustomersLoading,
    isError: isCustomersError,
  } = useCustomers();
  const {
    data: orders = [],
    isLoading: isOrdersLoading,
    isError: isOrdersError,
  } = useOrders();

  useEffect(() => {
    if (isOrdersLoading || isOrdersError || getValues("number")) {
      return;
    }

    setValue(
      "number",
      getNextOrderNumber(orders.map((order) => order.number)),
    );
  }, [getValues, isOrdersError, isOrdersLoading, orders, setValue]);

  const createCustomerMutation = useCreateCustomer({
    onSuccess: async (customer) => {
      await queryClient.invalidateQueries({ queryKey: ["customers"] });
      setValue("customerId", customer.id, { shouldValidate: true });
      setIsCreateCustomerOpen(false);
      requestAnimationFrame(() => customerSelectRef.current?.focus());
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
          inputRef={customerSelectRef}
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
