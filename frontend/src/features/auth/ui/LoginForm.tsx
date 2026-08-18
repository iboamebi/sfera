import { zodResolver } from "@hookform/resolvers/zod";
import { Button, Stack, TextField } from "@mui/material";
import { useForm } from "react-hook-form";

import { loginSchema } from "../model/schema";
import type { LoginFormValues } from "../model/schema";

interface LoginFormProps {
  onSubmit: (data: LoginFormValues) => void;
  isPending?: boolean;
}

export function LoginForm({ onSubmit, isPending = false }: LoginFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Stack spacing={2}>
        <TextField
          label="Имя пользователя"
          autoComplete="username"
          {...register("username")}
          error={Boolean(errors.username)}
          helperText={errors.username?.message}
          disabled={isPending}
          autoFocus
        />

        <TextField
          label="Пароль"
          type="password"
          autoComplete="current-password"
          {...register("password")}
          error={Boolean(errors.password)}
          helperText={errors.password?.message}
          disabled={isPending}
        />

        <Button type="submit" variant="contained" disabled={isPending}>
          {isPending ? "Вход..." : "Войти"}
        </Button>
      </Stack>
    </form>
  );
}
