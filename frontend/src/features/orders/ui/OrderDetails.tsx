import { Stack, Typography } from "@mui/material";

import type { OrderRead } from "../model/types";

interface OrderDetailsProps {
  order: OrderRead;
}

export function OrderDetails({
  order,
}: OrderDetailsProps) {
  return (
    <Stack spacing={1}>
      <Typography variant="h5">
        Order {order.number}
      </Typography>

      <Typography>
        ID: {order.id}
      </Typography>

      <Typography>
        Customer: {order.customerId}
      </Typography>

      <Typography>
        Status: {order.status}
      </Typography>

      <Typography>
        Received: {order.receivedAt}
      </Typography>

      <Typography>
        Planned issue: {order.plannedIssueAt ?? "-"}
      </Typography>

      <Typography>
        Issued: {order.issuedAt ?? "-"}
      </Typography>

      <Typography>
        Comment: {order.comment ?? "-"}
      </Typography>

      <Typography>
        Archived: {order.archived ? "Yes" : "No"}
      </Typography>
    </Stack>
  );
}
