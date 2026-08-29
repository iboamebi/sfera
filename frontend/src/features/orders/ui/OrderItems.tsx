import { Chip, Divider, Stack, Typography } from "@mui/material";

import type { OrderItem, OrderItemOperation } from "../model/types";

interface OrderItemsProps {
  items: OrderItem[];
}

const OPERATION_LABELS: Record<OrderItemOperation, string> = {
  verification: "Поверка",
  diagnostic: "Диагностика",
  repair: "Ремонт",
  sale: "Продажа",
};

export function OrderItems({ items }: OrderItemsProps) {
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
            <Typography variant="body1">Позиция {index + 1}</Typography>

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
