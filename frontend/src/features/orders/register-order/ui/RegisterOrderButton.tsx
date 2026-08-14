import { Button } from "@mui/material";

import { useRegisterOrder } from "../model/useRegisterOrder";

interface RegisterOrderButtonProps {
  orderId: string;
  onSuccess?: () => void;
}

export function RegisterOrderButton({
  orderId,
  onSuccess,
}: RegisterOrderButtonProps) {
  const mutation = useRegisterOrder({
    onSuccess,
  });

  return (
    <Button
      variant="contained"
      onClick={() => mutation.mutate(orderId)}
      disabled={mutation.isPending}
    >
      {mutation.isPending ? "Регистрация..." : "Зарегистрировать"}
    </Button>
  );
}
