import { Alert } from "@mui/material";

export function OrderListEmpty() {
  return (
    <Alert severity="info">
      Заказов нет.
    </Alert>
  );
}
