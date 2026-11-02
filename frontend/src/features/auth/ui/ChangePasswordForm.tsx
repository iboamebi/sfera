import { zodResolver } from "@hookform/resolvers/zod";
import { Alert, Button, Stack, TextField } from "@mui/material";
import { useForm } from "react-hook-form";

import { changePasswordSchema } from "../model/changePasswordSchema";
import type { ChangePasswordFormValues } from "../model/changePasswordSchema";

interface ChangePasswordFormProps {
  onSubmit: (data: ChangePasswordFormValues) => void;
  isPending: boolean;
  error: Error | null;
}

export function ChangePasswordForm({
  onSubmit,
  isPending,
  error,
}: ChangePasswordFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ChangePasswordFormValues>({
    resolver: zodResolver(changePasswordSchema),
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Stack spacing={2}>
        {error && (
          <Alert severity="error">
            Не удалось изменить пароль. Проверьте текущий пароль.
          </Alert>
        )}
        <TextField
          label="Текущий пароль"
          type="password"
          autoComplete="current-password"
          {...register("currentPassword")}
          error={Boolean(errors.currentPassword)}
          helperText={errors.currentPassword?.message}
          disabled={isPending}
          autoFocus
        />
        <TextField
          label="Новый пароль"
          type="password"
          autoComplete="new-password"
          {...register("newPassword")}
          error={Boolean(errors.newPassword)}
          helperText={errors.newPassword?.message}
          disabled={isPending}
        />
        <TextField
          label="Повторите новый пароль"
          type="password"
          autoComplete="new-password"
          {...register("confirmPassword")}
          error={Boolean(errors.confirmPassword)}
          helperText={errors.confirmPassword?.message}
          disabled={isPending}
        />
        <Button type="submit" variant="contained" disabled={isPending}>
          {isPending ? "Сохранение..." : "Изменить пароль"}
        </Button>
      </Stack>
    </form>
  );
}
