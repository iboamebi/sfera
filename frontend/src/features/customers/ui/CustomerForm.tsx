import { zodResolver } from "@hookform/resolvers/zod";
import { Button, Stack, TextField } from "@mui/material";
import { useForm } from "react-hook-form";

import {
  createCustomerSchema,
  type CreateCustomerSchema,
} from "../model/schema";

interface CustomerFormProps {
  onSubmit: (data: CreateCustomerSchema) => void;
  isPending?: boolean;
}

export function CustomerForm({
  onSubmit,
  isPending = false,
}: CustomerFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<CreateCustomerSchema>({
    resolver: zodResolver(createCustomerSchema),
    defaultValues: {
      discountPercent: 0,
    },
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Stack spacing={2}>
        <TextField
          label="Название"
          {...register("name")}
          error={Boolean(errors.name)}
          helperText={errors.name?.message}
          disabled={isPending}
        />

        <TextField
          label="Контактное лицо"
          {...register("contactPerson")}
          error={Boolean(errors.contactPerson)}
          helperText={errors.contactPerson?.message}
          disabled={isPending}
        />

        <TextField
          label="Телефон"
          {...register("phone")}
          error={Boolean(errors.phone)}
          helperText={errors.phone?.message}
          disabled={isPending}
        />

        <TextField
          label="Email"
          type="email"
          {...register("email")}
          error={Boolean(errors.email)}
          helperText={errors.email?.message}
          disabled={isPending}
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

        <TextField
          label="Скидка, %"
          type="number"
          slotProps={{ input: { inputProps: { min: 0, max: 100, step: 0.01 } } }}
          {...register("discountPercent", { valueAsNumber: true })}
          error={Boolean(errors.discountPercent)}
          helperText={errors.discountPercent?.message}
          disabled={isPending}
        />

        <Button
          type="submit"
          variant="contained"
          disabled={isPending}
        >
          {isPending ? "Создание..." : "Создать клиента"}
        </Button>
      </Stack>
    </form>
  );
}
