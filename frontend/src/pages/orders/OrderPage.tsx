import { Alert, Stack, Typography } from "@mui/material";
import { useParams } from "react-router";

import { useOrder } from "../../features/orders/model/useOrder";

export function OrderPage() {
  const { orderId } = useParams<{ orderId: string }>();
  const { data, error, isLoading } = useOrder(orderId ?? "");

  if (isLoading) {
    return <Typography>Loading...</Typography>;
  }

  if (error) {
    return <Alert severity="error">Failed to load order.</Alert>;
  }

  if (!data) {
    return <Alert severity="warning">Order not found.</Alert>;
  }

  return (
    <Stack spacing={1}>
      <Typography variant="h5">
        Order {data.number}
      </Typography>

      <Typography>
        ID: {data.id}
      </Typography>

      <Typography>
        Customer: {data.customerId}
      </Typography>

      <Typography>
        Status: {data.status}
      </Typography>

      <Typography>
        Received: {data.receivedAt}
      </Typography>

      <Typography>
        Planned issue: {data.plannedIssueAt ?? "-"}
      </Typography>

      <Typography>
        Issued: {data.issuedAt ?? "-"}
      </Typography>

      <Typography>
        Comment: {data.comment ?? "-"}
      </Typography>

      <Typography>
        Archived: {data.archived ? "Yes" : "No"}
      </Typography>
    </Stack>
  );
}
