import { Chip, Divider, Stack, Typography } from "@mui/material";

import { DeleteOrderItemButton } from "../delete-order-item/ui/DeleteOrderItemButton";
import type { OrderItem, OrderItemOperation } from "../model/types";

interface OrderItemsProps {
  items: OrderItem[];
  deletingItemId?: string | null;
  onDelete?: (itemId: string) => void;
}

const OPERATION_LABELS: Record<OrderItemOperation, string> = {
  verification: "Поверка",
  diagnostic: "Диагностика",
  repair: "Ремонт",
  sale: "Продажа",
};

export function OrderItems({
  items,
  deletingItemId = null,
  onDelete,
}: OrderItemsProps) {
  return (
    <Stack spacing={2}>
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
              sx={{
                alignItems: "center",
                justifyContent: "space-between",
              }}
            >
              <Typography variant="body1">Позиция {index + 1}</Typography>

              {onDelete && (
                <DeleteOrderItemButton
                  isPending={deletingItemId === item.id}
                  onClick={() => onDelete(item.id)}
                />
              )}
            </Stack>

            <Typography color="text.secondary" variant="body2">
              {item.instrumentTypeName ?? "СИ"}: {item.serialNumber ?? "—"}
            </Typography>

            <Stack
              direction="row"
              sx={{ flexWrap: "wrap", gap: 0.5 }}
            >
              {item.requestedOperations.map((operation) => (
                <Chip
                  key={operation}
                  label={OPERATION_LABELS[operation]}
                  size="small"
                />
              ))}
            </Stack>

            <Typography variant="body2">{item.comment || "—"}</Typography>

            {index < items.length - 1 && <Divider sx={{ pt: 1 }} />}
          </Stack>
        ))
      )}
    </Stack>
  );
}
