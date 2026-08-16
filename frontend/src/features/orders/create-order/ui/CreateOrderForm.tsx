import { zodResolver } from "@hookform/resolvers/zod";
import { Button, Stack, TextField } from "@mui/material";
import { useForm } from "react-hook-form";

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
          label="ID клиента"
          {...register("customerId")}
          error={Boolean(errors.customerId)}
          helperText={errors.customerId?.message}
          disabled={isPending}
        />
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
        <Button type="submit" variant="contained" disabled={isPending}>
          {isPending ? "Создание..." : "Создать заказ"}
        </Button>
      </Stack>
    </form>
  );
}
