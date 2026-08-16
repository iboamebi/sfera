import { Button, Stack, TextField } from "@mui/material";
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
    formState: { errors },
  } = useForm<UpdateOrderSchema>({
    resolver: zodResolver(updateOrderSchema),
    defaultValues: {
      plannedIssueAt: order.plannedIssueAt
        ? order.plannedIssueAt.slice(0, 16)
        : "",
      comment: order.comment ?? "",
    },
  });

  return (
    <Stack
      component="form"
      spacing={2}
      onSubmit={handleSubmit(onSubmit)}
    >
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
        disabled={isPending}
      >
        {isPending ? "Сохранение..." : "Сохранить"}
      </Button>
    </Stack>
  );
}
