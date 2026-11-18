import { useState } from "react";
import { Link as RouterLink } from "react-router";
import {
  Button,
  Link,
  MenuItem,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";

import {
  type WarehouseMovementFilters,
  type WarehouseMovementType,
} from "../api/warehouseMovementApi";
import type { WarehouseStockRead } from "../model/types";
import { useWarehouseMovements } from "../queries/useWarehouseMovements";

interface WarehouseMovementTableProps {
  warehouseId: string;
  stocks: WarehouseStockRead[];
}

const movementLabels: Record<WarehouseMovementType, string> = {
  RECEIPT: "Поступление",
  ISSUE: "Выдача",
  RESERVATION: "Резерв",
  RELEASE: "Снятие резерва",
  ADJUSTMENT: "Корректировка",
};

export function WarehouseMovementTable({
  warehouseId,
  stocks,
}: WarehouseMovementTableProps) {
  const [filters, setFilters] = useState<WarehouseMovementFilters>({
    limit: 50,
    offset: 0,
  });
  const { data, isLoading, isError } = useWarehouseMovements(
    warehouseId,
    filters,
  );

  const updateFilter = (patch: Partial<WarehouseMovementFilters>) => {
    setFilters((current) => ({ ...current, ...patch, offset: 0 }));
  };

  const page = data;
  const canGoBack = (filters.offset ?? 0) > 0;
  const canGoForward = Boolean(
    page && (filters.offset ?? 0) + page.items.length < page.total,
  );

  return (
    <Stack spacing={2} sx={{ mt: 4 }}>
      <Typography variant="h6">История движений</Typography>
      <Stack direction={{ xs: "column", md: "row" }} spacing={2}>
        <TextField
          select
          label="Материал"
          size="small"
          value={filters.materialId ?? ""}
          onChange={(event) =>
            updateFilter({ materialId: event.target.value || undefined })
          }
          sx={{ minWidth: 220 }}
        >
          <MenuItem value="">Все материалы</MenuItem>
          {stocks.map((stock) => (
            <MenuItem key={stock.materialId} value={stock.materialId}>
              {stock.materialName}
            </MenuItem>
          ))}
        </TextField>
        <TextField
          select
          label="Тип движения"
          size="small"
          value={filters.movementType ?? ""}
          onChange={(event) =>
            updateFilter({
              movementType:
                (event.target.value as WarehouseMovementType) || undefined,
            })
          }
          sx={{ minWidth: 200 }}
        >
          <MenuItem value="">Все типы</MenuItem>
          {Object.entries(movementLabels).map(([value, label]) => (
            <MenuItem key={value} value={value}>
              {label}
            </MenuItem>
          ))}
        </TextField>
        <TextField
          label="С даты"
          type="date"
          size="small"
          value={filters.dateFrom ?? ""}
          onChange={(event) =>
            updateFilter({
              dateFrom: event.target.value || undefined,
            })
          }
          slotProps={{ inputLabel: { shrink: true } }}
        />
        <TextField
          label="По дату"
          type="date"
          size="small"
          value={filters.dateTo ?? ""}
          onChange={(event) =>
            updateFilter({
              dateTo: event.target.value || undefined,
            })
          }
          slotProps={{ inputLabel: { shrink: true } }}
        />
        <Button
          variant="text"
          onClick={() => setFilters({ limit: 50, offset: 0 })}
        >
          Сбросить
        </Button>
      </Stack>

      {isLoading ? (
        <Typography>Загрузка истории...</Typography>
      ) : isError ? (
        <Typography color="error">Не удалось загрузить историю движений.</Typography>
      ) : (
        <>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Дата</TableCell>
                <TableCell>Материал</TableCell>
                <TableCell>Операция</TableCell>
                <TableCell align="right">Количество</TableCell>
                <TableCell>Заказ</TableCell>
                <TableCell>Комментарий</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {page?.items.map((item) => (
                <TableRow key={item.id}>
                  <TableCell>
                    {new Date(item.createdAt).toLocaleString("ru-RU")}
                  </TableCell>
                  <TableCell>{item.materialName}</TableCell>
                  <TableCell>{movementLabels[item.movementType]}</TableCell>
                  <TableCell align="right">{item.quantity}</TableCell>
                  <TableCell>
                    {item.orderId && item.orderNumber ? (
                      <Link component={RouterLink} to={`/orders/${item.orderId}`}>
                        № {item.orderNumber}
                      </Link>
                    ) : (
                      "—"
                    )}
                  </TableCell>
                  <TableCell>{item.comment ?? "—"}</TableCell>
                </TableRow>
              ))}
              {!page?.items.length && (
                <TableRow>
                  <TableCell colSpan={6} align="center">
                    Движений не найдено
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
          <Stack direction="row" spacing={2} sx={{ alignItems: "center", justifyContent: "flex-end" }}>
            <Typography variant="body2">
              {page?.total ?? 0} записей
            </Typography>
            <Button
              disabled={!canGoBack}
              onClick={() =>
                setFilters((current) => ({
                  ...current,
                  offset: Math.max(0, (current.offset ?? 0) - (current.limit ?? 50)),
                }))
              }
            >
              Назад
            </Button>
            <Button
              disabled={!canGoForward}
              onClick={() =>
                setFilters((current) => ({
                  ...current,
                  offset: (current.offset ?? 0) + (current.limit ?? 50),
                }))
              }
            >
              Далее
            </Button>
          </Stack>
        </>
      )}
    </Stack>
  );
}
