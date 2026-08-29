import { Button } from "@mui/material";

interface DeleteOrderItemButtonProps {
  isPending?: boolean;
  onClick: () => void;
}

export function DeleteOrderItemButton({
  isPending = false,
  onClick,
}: DeleteOrderItemButtonProps) {
  return (
    <Button
      color="error"
      disabled={isPending}
      onClick={onClick}
      size="small"
      variant="text"
    >
      {isPending ? "Удаление…" : "Удалить"}
    </Button>
  );
}
