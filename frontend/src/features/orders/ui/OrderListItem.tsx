import { Stack, Typography } from "@mui/material";
import { Link } from "react-router";

import type { OrderRead } from "../model/types";

interface OrderListItemProps {
  order: OrderRead;
}

export function OrderListItem({ order }: OrderListItemProps) {
  return (
    <Stack
      spacing={2}
      sx={{
        display: "flex",
        flexDirection: "row",
        alignItems: "center",
        justifyContent: "space-between",
      }}
    >
      <Typography>
        <Link to={`/orders/${order.id}`}>{order.number}</Link> — {order.customerName} — {order.status}
      </Typography>
    </Stack>
  );
}
