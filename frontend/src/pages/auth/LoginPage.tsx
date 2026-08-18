import { Alert, Stack, Typography } from "@mui/material";
import { useNavigate } from "react-router";

import { useLogin } from "../../features/auth/model/useLogin";
import type { LoginFormValues } from "../../features/auth/model/schema";
import { LoginForm } from "../../features/auth/ui/LoginForm";

export function LoginPage() {
  const navigate = useNavigate();
  const { mutate, isPending, error } = useLogin();

  const handleSubmit = (data: LoginFormValues) => {
    mutate(data, {
      onSuccess: () => navigate("/orders"),
    });
  };

  return (
    <Stack spacing={3}>
      <Typography variant="h4">Вход</Typography>
      {error && <Alert severity="error">Не удалось выполнить вход</Alert>}
      <LoginForm onSubmit={handleSubmit} isPending={isPending} />
    </Stack>
  );
}
