import { Button, Stack, Typography } from "@mui/material";
import { Link } from "react-router";

import type { OrderRead } from "../model/types";

interface OrderListItemProps {
  order: OrderRead;
}

export function OrderListItem({ order }: OrderListItemProps) {
  return (
    <Stack
      direction="row"
      alignItems="center"
      justifyContent="space-between"
      spacing={2}
    >
      <Typography>
        {order.number} — {order.status}
      </Typography>

      <Button
        component={Link}
        to={`/orders/${order.id}`}
        variant="outlined"
        size="small"
        sx={{ flexShrink: 0 }}
      >
        Открыть
      </Button>
    </Stack>
  );
}
