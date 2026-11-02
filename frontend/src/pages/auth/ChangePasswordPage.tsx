import { Stack, Typography } from "@mui/material";
import { useNavigate } from "react-router";

import { useChangePassword } from "../../features/auth/model/useChangePassword";
import type { ChangePasswordFormValues } from "../../features/auth/model/changePasswordSchema";
import { ChangePasswordForm } from "../../features/auth/ui/ChangePasswordForm";

export function ChangePasswordPage() {
  const navigate = useNavigate();
  const { mutate, isPending, error } = useChangePassword();

  const handleSubmit = ({
    currentPassword,
    newPassword,
  }: ChangePasswordFormValues) => {
    mutate(
      { currentPassword, newPassword },
      {
        onSuccess: () => navigate("/orders", { replace: true }),
      },
    );
  };

  return (
    <Stack spacing={3} sx={{ maxWidth: 480 }}>
      <Typography variant="h4">Смена пароля</Typography>
      <Typography>
        Перед началом работы необходимо установить новый пароль.
      </Typography>
      <ChangePasswordForm
        onSubmit={handleSubmit}
        isPending={isPending}
        error={error}
      />
    </Stack>
  );
}
