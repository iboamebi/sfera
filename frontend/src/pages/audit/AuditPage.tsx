import { useState } from "react";
import {
  Alert,
  Button,
  Collapse,
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";

import { useAuditRecords } from "../../features/audit/model/useAuditRecords";
import type { AuditFilters, AuditRecord } from "../../features/audit/model/types";

const DEFAULT_FILTERS: AuditFilters = {
  occurredFrom: "",
  occurredTo: "",
  actorId: "",
  action: "",
  entityType: "",
  operationId: "",
  limit: 50,
  offset: 0,
};

function formatDateTime(value: string): string {
  return new Intl.DateTimeFormat("ru-RU", {
    dateStyle: "short",
    timeStyle: "medium",
  }).format(new Date(value));
}

function actorLabel(username: string | null, fullName: string | null, id: string): string {
  const name = [fullName, username].filter(Boolean).join(" · ");
  return name ? `${name} (${id})` : id;
}

function AuditRecordDetails({ record }: { record: AuditRecord }) {
  return (
    <Stack spacing={1.5} sx={{ p: 2, bgcolor: "action.hover" }}>
      <Typography variant="subtitle2">Детали записи</Typography>
      <Typography variant="body2">
        <strong>Инициатор операции:</strong>{" "}
        {record.initiatedBy
          ? actorLabel(record.initiatorUsername, record.initiatorFullName, record.initiatedBy)
          : "—"}
      </Typography>
      <Typography variant="body2">
        <strong>ID операции:</strong> {record.operationId}
      </Typography>
      <Typography variant="body2">
        <strong>ID записи:</strong> {record.id}
      </Typography>
      <Typography variant="body2">
        <strong>ID сущности:</strong> {record.entityId ?? "—"}
      </Typography>
      <Typography variant="body2">
        <strong>Связанная запись:</strong> {record.relatedRecordId ?? "—"}
      </Typography>
      <Typography variant="body2">
        <strong>Причина:</strong> {record.reason || "Не указана"}
      </Typography>
      <Typography variant="subtitle2">Изменения</Typography>
      {Object.keys(record.changes).length === 0 ? (
        <Typography variant="body2" color="text.secondary">
          Данные об изменениях отсутствуют.
        </Typography>
      ) : (
        <Paper variant="outlined" sx={{ p: 1.5, overflowX: "auto" }}>
          <pre style={{ margin: 0, whiteSpace: "pre-wrap", overflowWrap: "anywhere" }}>
            {JSON.stringify(record.changes, null, 2)}
          </pre>
        </Paper>
      )}
    </Stack>
  );
}

export function AuditPage() {
  const [filters, setFilters] = useState<AuditFilters>(DEFAULT_FILTERS);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const { data, isLoading, isError, error } = useAuditRecords(filters);

  const updateFilter = (field: keyof AuditFilters, value: string) => {
    setFilters((current) => ({
      ...current,
      [field]: value,
      offset: 0,
    }));
  };

  const resetFilters = () => {
    setFilters(DEFAULT_FILTERS);
    setExpandedId(null);
  };

  const pageCount = data ? Math.max(1, Math.ceil(data.total / filters.limit)) : 1;
  const currentPage = Math.floor(filters.offset / filters.limit) + 1;

  return (
    <Stack spacing={3}>
      <Typography variant="h4">Журнал аудита</Typography>

      <Paper variant="outlined" sx={{ p: 2 }}>
        <Stack spacing={2}>
          <Typography variant="h6">Фильтры</Typography>
          <Stack direction={{ xs: "column", md: "row" }} spacing={2}>
            <TextField
              label="С"
              type="datetime-local"
              size="small"
              value={filters.occurredFrom}
              onChange={(event) => updateFilter("occurredFrom", event.target.value)}
              slotProps={{ inputLabel: { shrink: true } }}
              fullWidth
            />
            <TextField
              label="По"
              type="datetime-local"
              size="small"
              value={filters.occurredTo}
              onChange={(event) => updateFilter("occurredTo", event.target.value)}
              slotProps={{ inputLabel: { shrink: true } }}
              fullWidth
            />
            <TextField
              label="ID пользователя"
              size="small"
              value={filters.actorId}
              onChange={(event) => updateFilter("actorId", event.target.value)}
              fullWidth
            />
          </Stack>
          <Stack direction={{ xs: "column", md: "row" }} spacing={2}>
            <TextField
              label="Действие (точное значение)"
              size="small"
              value={filters.action}
              onChange={(event) => updateFilter("action", event.target.value)}
              fullWidth
            />
            <TextField
              label="Тип сущности (точное значение)"
              size="small"
              value={filters.entityType}
              onChange={(event) => updateFilter("entityType", event.target.value)}
              fullWidth
            />
            <TextField
              label="ID операции"
              size="small"
              value={filters.operationId}
              onChange={(event) => updateFilter("operationId", event.target.value)}
              fullWidth
            />
          </Stack>
          <Stack direction="row" spacing={1} justifyContent="flex-end">
            <Button onClick={resetFilters}>Сбросить</Button>
          </Stack>
        </Stack>
      </Paper>

      {isError && (
        <Alert severity="error">
          Не удалось загрузить журнал аудита. Проверьте права администратора и корректность фильтров.
          {error instanceof Error ? ` ${error.message}` : ""}
        </Alert>
      )}

      {isLoading && <Typography>Загрузка журнала аудита...</Typography>}

      {data && (
        <>
          <Stack direction="row" justifyContent="space-between" alignItems="center">
            <Typography color="text.secondary">
              Записей: {data.total.toLocaleString("ru-RU")}
            </Typography>
            <Typography color="text.secondary" variant="body2">
              Страница {currentPage} из {pageCount}
            </Typography>
          </Stack>

          {data.items.length === 0 ? (
            <Typography color="text.secondary">
              По заданным условиям записи не найдены.
            </Typography>
          ) : (
            <TableContainer component={Paper} variant="outlined">
              <Table size="small" sx={{ minWidth: 1050 }}>
                <TableHead>
                  <TableRow>
                    <TableCell>Дата и время</TableCell>
                    <TableCell>Пользователь</TableCell>
                    <TableCell>Действие</TableCell>
                    <TableCell>Тип сущности</TableCell>
                    <TableCell>ID сущности</TableCell>
                    <TableCell>Детали</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {data.items.map((record) => (
                    <>
                      <TableRow
                        key={record.id}
                        hover
                        selected={expandedId === record.id}
                      >
                        <TableCell sx={{ whiteSpace: "nowrap" }}>
                          {formatDateTime(record.occurredAt)}
                        </TableCell>
                        <TableCell sx={{ minWidth: 220 }}>
                          {actorLabel(record.actorUsername, record.actorFullName, record.actorId)}
                        </TableCell>
                        <TableCell>{record.action}</TableCell>
                        <TableCell>{record.entityType}</TableCell>
                        <TableCell sx={{ maxWidth: 180, overflowWrap: "anywhere" }}>
                          {record.entityId ?? "—"}
                        </TableCell>
                        <TableCell>
                          <Button
                            size="small"
                            onClick={() =>
                              setExpandedId((current) =>
                                current === record.id ? null : record.id,
                              )
                            }
                          >
                            {expandedId === record.id ? "Скрыть" : "Открыть"}
                          </Button>
                        </TableCell>
                      </TableRow>
                      <TableRow key={`${record.id}-details`}>
                        <TableCell colSpan={6} sx={{ p: 0, borderBottom: 0 }}>
                          <Collapse in={expandedId === record.id} unmountOnExit>
                            <AuditRecordDetails record={record} />
                          </Collapse>
                        </TableCell>
                      </TableRow>
                    </>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}

          <Stack direction="row" spacing={2} justifyContent="flex-end" alignItems="center">
            <Button
              disabled={filters.offset === 0 || isLoading}
              onClick={() =>
                setFilters((current) => ({
                  ...current,
                  offset: Math.max(0, current.offset - current.limit),
                }))
              }
            >
              Назад
            </Button>
            <Button
              disabled={filters.offset + filters.limit >= data.total || isLoading}
              onClick={() =>
                setFilters((current) => ({
                  ...current,
                  offset: current.offset + current.limit,
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
