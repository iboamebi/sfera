import { Button } from "@mui/material";

interface RegisterOrderButtonProps {
  onClick: () => void;
  isPending: boolean;
}

export function RegisterOrderButton({
  onClick,
  isPending,
}: RegisterOrderButtonProps) {
  return (
    <Button
      variant="contained"
      onClick={onClick}
      disabled={isPending}
    >
      {isPending ? "Регистрация..." : "Зарегистрировать"}
    </Button>
  );
}
