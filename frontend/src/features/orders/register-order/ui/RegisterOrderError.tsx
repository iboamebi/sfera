import { Alert } from "@mui/material";

export function RegisterOrderError() {
  return (
    <Alert severity="error">
      Failed to register order.
    </Alert>
  );
}
