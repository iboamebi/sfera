import { zodResolver } from "@hookform/resolvers/zod";
import { Button, Stack, TextField } from "@mui/material";
import { useForm } from "react-hook-form";

import { createOrderSchema } from "../model/schema";
import type { CreateOrderForm as CreateOrderFormValues } from "../model/types";

interface CreateOrderFormProps {
  onSubmit: (data: CreateOrderFormValues) => void;
}

export function CreateOrderForm({ onSubmit }: CreateOrderFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<CreateOrderFormValues>({
    resolver: zodResolver(createOrderSchema),
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Stack spacing={2}>
        <TextField
          label="Номер заказа"
          {...register("number")}
          error={Boolean(errors.number)}
          helperText={errors.number?.message}
        />
        <TextField
          label="ID клиента"
          {...register("customerId")}
          error={Boolean(errors.customerId)}
          helperText={errors.customerId?.message}
        />
        <Button type="submit" variant="contained">
          Создать заказ
        </Button>
      </Stack>
    </form>
  );
}
