import { Button, Divider, Stack, Typography } from "@mui/material";

import type { OrderItem } from "../model/types";

interface OrderItemsProps {
  items: OrderItem[];
  canRemove?: boolean;
  isRemoving?: boolean;
  onRemove?: (itemId: string) => void;
}

export function OrderItems({
  items,
  canRemove = false,
  isRemoving = false,
  onRemove,
}: OrderItemsProps) {
  return (
    <Stack spacing={2} sx={{ flex: 1 }}>
      <Typography variant="h6">Позиции заказа</Typography>

      {items.length === 0 ? (
        <Typography color="text.secondary" variant="body2">
          Позиции отсутствуют
        </Typography>
      ) : (
        items.map((item, index) => (
          <Stack key={item.id} spacing={0.5}>
            <Stack
              direction="row"
              spacing={2}
              sx={{ alignItems: "center", justifyContent: "space-between" }}
            >
              <Typography variant="body1">Позиция {index + 1}</Typography>

              {canRemove && onRemove && (
                <Button
                  disabled={isRemoving}
                  onClick={() => onRemove(item.id)}
                  size="small"
                >
                  Удалить
                </Button>
              )}
            </Stack>

            <Typography color="text.secondary" variant="body2">
              {item.instrumentTypeName ?? "СИ"}: {item.serialNumber ?? "—"}
            </Typography>

            <Typography variant="body2">{item.comment || "—"}</Typography>

            {index < items.length - 1 && <Divider sx={{ pt: 1 }} />}
          </Stack>
        ))
      )}
    </Stack>
  );
}
