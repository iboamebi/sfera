import { useMemo, useState } from "react";
import {
  FormControl,
  InputLabel,
  MenuItem,
  Paper,
  Select,
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
import { Link } from "react-router";

import { useVerifications } from "../../features/verifications/model/useVerifications";
import type {
  VerificationListRead,
  VerificationResult,
  VerificationStatus,
} from "../../features/verifications/model/types";

const STATUS_LABELS: Record<VerificationStatus, string> = {
  CREATED: "Создана",
  IN_PROGRESS: "В работе",
  DECIDED: "Решение принято",
  CANCELLED: "Отменена",
};

const RESULT_LABELS: Record<VerificationResult, string> = {
  SUITABLE: "Пригодно",
  UNSUITABLE: "Непригодно",
};

const TYPE_LABELS: Record<VerificationListRead["verificationType"], string> = {
  PRIMARY: "Первичная",
  PERIODIC: "Периодическая",
  AFTER_REPAIR: "После ремонта",
};

function formatDate(value: string | null): string {
  if (!value) return "—";
  const [year, month, day] = value.slice(0, 10).split("-");
  return year && month && day ? `${day}.${month}.${year}` : value;
}

function getSearchValues(verification: VerificationListRead): string[] {
  return [
    verification.orderNumber,
    verification.customerName,
    verification.instrumentName,
    verification.instrumentTypeName,
    verification.serialNumber,
    TYPE_LABELS[verification.verificationType],
    STATUS_LABELS[verification.status],
    verification.result ? RESULT_LABELS[verification.result] : "Без решения",
  ].filter((value): value is string => value !== null);
}

export function VerificationsPage() {
  const { data: verifications, isLoading, error } = useVerifications();
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState<VerificationStatus | "ALL">("ALL");
  const [result, setResult] = useState<VerificationResult | "ALL" | "NONE">("ALL");

  const filteredVerifications = useMemo(() => {
    const query = search.trim().toLocaleLowerCase("ru-RU");

    return (verifications ?? []).filter((verification) => {
      const matchesSearch =
        !query ||
        getSearchValues(verification).some((value) =>
          value.toLocaleLowerCase("ru-RU").includes(query),
        );

      const matchesStatus =
        status === "ALL" || verification.status === status;

      const matchesResult =
        result === "ALL" ||
        (result === "NONE" && verification.result === null) ||
        verification.result === result;

      return matchesSearch && matchesStatus && matchesResult;
    });
  }, [result, search, status, verifications]);

  if (isLoading) {
    return <Typography>Загрузка поверок...</Typography>;
  }

  if (error) {
    return <Typography>Не удалось загрузить поверки.</Typography>;
  }

  return (
    <Stack spacing={3}>
      <Typography variant="h4">Поверки</Typography>

      <Stack
        direction={{ xs: "column", md: "row" }}
        spacing={2}
        sx={{ alignItems: { md: "center" } }}
      >
        <TextField
          label="Поиск"
          placeholder="Заказ, клиент, СИ, тип или заводской номер"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          size="small"
          fullWidth
        />

        <FormControl size="small" sx={{ minWidth: 190 }}>
          <InputLabel id="verification-status-filter">Статус</InputLabel>
          <Select
            labelId="verification-status-filter"
            value={status}
            label="Статус"
            onChange={(event) =>
              setStatus(event.target.value as VerificationStatus | "ALL")
            }
          >
            <MenuItem value="ALL">Все статусы</MenuItem>
            <MenuItem value="CREATED">Создана</MenuItem>
            <MenuItem value="IN_PROGRESS">В работе</MenuItem>
            <MenuItem value="DECIDED">Решение принято</MenuItem>
            <MenuItem value="CANCELLED">Отменена</MenuItem>
          </Select>
        </FormControl>

        <FormControl size="small" sx={{ minWidth: 180 }}>
          <InputLabel id="verification-result-filter">Результат</InputLabel>
          <Select
            labelId="verification-result-filter"
            value={result}
            label="Результат"
            onChange={(event) =>
              setResult(
                event.target.value as VerificationResult | "ALL" | "NONE",
              )
            }
          >
            <MenuItem value="ALL">Все результаты</MenuItem>
            <MenuItem value="SUITABLE">Пригодно</MenuItem>
            <MenuItem value="UNSUITABLE">Непригодно</MenuItem>
            <MenuItem value="NONE">Без решения</MenuItem>
          </Select>
        </FormControl>
      </Stack>

      {verifications && verifications.length === 0 && (
        <Typography color="text.secondary">Поверки пока не созданы.</Typography>
      )}

      {verifications &&
        verifications.length > 0 &&
        filteredVerifications.length === 0 && (
          <Typography color="text.secondary">
            По заданным условиям поверки не найдены.
          </Typography>
        )}

      {filteredVerifications.length > 0 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small" sx={{ minWidth: 1100 }}>
            <TableHead>
              <TableRow>
                <TableCell sx={{ fontWeight: 700, whiteSpace: "nowrap" }}>
                  Дата поверки
                </TableCell>
                <TableCell sx={{ fontWeight: 700, whiteSpace: "nowrap" }}>
                  Заказ
                </TableCell>
                <TableCell sx={{ fontWeight: 700 }}>Клиент</TableCell>
                <TableCell sx={{ fontWeight: 700 }}>СИ</TableCell>
                <TableCell sx={{ fontWeight: 700 }}>Тип</TableCell>
                <TableCell sx={{ fontWeight: 700 }}>Статус</TableCell>
                <TableCell sx={{ fontWeight: 700 }}>Результат</TableCell>
                <TableCell sx={{ fontWeight: 700, whiteSpace: "nowrap" }}>
                  Действительна до
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredVerifications.map((verification) => (
                <TableRow key={verification.id} hover>
                  <TableCell>
                    <Link to={`/verifications/${verification.id}`}>
                      {formatDate(verification.verificationDate)}
                    </Link>
                  </TableCell>
                  <TableCell>
                    <Link to={`/orders/${verification.orderId}`}>
                      {verification.orderNumber}
                    </Link>
                  </TableCell>
                  <TableCell>{verification.customerName}</TableCell>
                  <TableCell>
                    <Stack spacing={0.25}>
                      <Typography variant="body2">
                        {verification.instrumentName ||
                          verification.instrumentTypeName ||
                          "—"}
                      </Typography>
                      {verification.serialNumber && (
                        <Typography variant="caption" color="text.secondary">
                          Зав. № {verification.serialNumber}
                        </Typography>
                      )}
                    </Stack>
                  </TableCell>
                  <TableCell>
                    {TYPE_LABELS[verification.verificationType]}
                  </TableCell>
                  <TableCell>{STATUS_LABELS[verification.status]}</TableCell>
                  <TableCell>
                    {verification.result
                      ? RESULT_LABELS[verification.result]
                      : "—"}
                  </TableCell>
                  <TableCell>{formatDate(verification.validUntil)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Stack>
  );
}
