import { Button, Stack, TextField } from "@mui/material";
import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

import type { OrderRead } from "../../model/types";
import {
  updateOrderSchema,
  type UpdateOrderSchema,
} from "../model/schema";

interface UpdateOrderFormProps {
  order: OrderRead;
  onSubmit: (data: UpdateOrderSchema) => void;
  isPending?: boolean;
}

export function UpdateOrderForm({
  order,
  onSubmit,
  isPending = false,
}: UpdateOrderFormProps) {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isDirty },
  } = useForm<UpdateOrderSchema>({
    resolver: zodResolver(updateOrderSchema),
    defaultValues: {
      plannedIssueAt: order.plannedIssueAt
        ? order.plannedIssueAt.slice(0, 16)
        : "",
    },
  });

  useEffect(() => {
    reset({
      plannedIssueAt: order.plannedIssueAt
        ? order.plannedIssueAt.slice(0, 16)
        : "",
    });
  }, [order.plannedIssueAt, reset]);

  return (
    <Stack
      component="form"
      spacing={2}
      onSubmit={handleSubmit(onSubmit)}
    >
      <TextField
        label="Планируемая выдача"
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

      {isDirty && (
        <Button
          type="submit"
          variant="contained"
          disabled={isPending}
          sx={{ alignSelf: "flex-start" }}
        >
          {isPending ? "Сохранение..." : "Сохранить"}
        </Button>
      )}
    </Stack>
  );
}
