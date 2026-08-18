import { Alert, Stack, Typography } from "@mui/material";
import { useNavigate } from "react-router";

import { useLogin } from "../../features/auth/model/useLogin";
import { LoginForm } from "../../features/auth/ui/LoginForm";

export function LoginPage() {
  const navigate = useNavigate();
  const { mutate, isPending, error } = useLogin();

  return (
    <Stack spacing={3}>
      <Typography variant="h4">Вход</Typography>
      {error && <Alert severity="error">Не удалось выполнить вход</Alert>}
      <LoginForm
        onSubmit={mutate}
        isPending={isPending}
        onSuccess={() => navigate("/orders")}
      />
    </Stack>
  );
}
