import { Alert } from "@mui/material";

export function UpdateOrderError() {
  return (
    <Alert severity="error">
      Не удалось обновить заказ.
    </Alert>
  );
}
