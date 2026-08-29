import { Button } from "@mui/material";

interface RegisterOrderButtonProps {
  onClick: () => void;
  isPending: boolean;
  disabled?: boolean;
}

export function RegisterOrderButton({
  onClick,
  isPending,
  disabled = false,
}: RegisterOrderButtonProps) {
  return (
    <Button
      variant="contained"
      onClick={onClick}
      disabled={isPending || disabled}
    >
      {isPending ? "Регистрация..." : "Зарегистрировать"}
    </Button>
  );
}
