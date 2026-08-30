import { Alert, Card, CardContent, Divider, Stack, Typography } from "@mui/material";
import { useState } from "react";

import { AddOrderItemButton } from "../add-order-item/ui/AddOrderItemButton";
import { AddOrderItemsForm } from "../add-order-items/ui/AddOrderItemsForm";
import { useDeleteOrderItem } from "../delete-order-item/model/useDeleteOrderItem";
import { OrderItems } from "./OrderItems";
import type { OrderRead } from "../model/types";

interface OrderDetailsProps {
  order: OrderRead;
}

export function OrderDetails({ order }: OrderDetailsProps) {
  const deleteOrderItemMutation = useDeleteOrderItem(order.id);
  const [error, setError] = useState(false);

  const handleDeleteItem = (itemId: string) => {
    setError(false);
    deleteOrderItemMutation.mutate(itemId, { onError: () => setError(true) });
  };

  return (
    <Card>
      <CardContent>
        <Stack spacing={2}>
          <Typography variant="h5">Заказ №{order.number}</Typography>
          {error && <Alert severity="error">Не удалось удалить позицию заказа.</Alert>}
          <Stack direction="row" spacing={2} sx={{ alignItems: "flex-start", justifyContent: "space-between" }}>
            <OrderItems
              orderId={order.id}
              items={order.items}
              deletingItemId={deleteOrderItemMutation.isPending ? deleteOrderItemMutation.variables ?? null : null}
              onDelete={order.status === "NEW" ? handleDeleteItem : undefined}
            />
            {order.status === "NEW" && (
              <Stack spacing={2}>
                <AddOrderItemButton orderId={order.id} />
                <Divider />
                <AddOrderItemsForm orderId={order.id} />
              </Stack>
            )}
          </Stack>
        </Stack>
      </CardContent>
    </Card>
  );
}
