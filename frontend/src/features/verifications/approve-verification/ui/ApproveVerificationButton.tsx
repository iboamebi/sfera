import { useMemo, useState } from "react";

import { Alert, Button, Stack, TextField, Typography } from "@mui/material";
import { useQueryClient } from "@tanstack/react-query";

import { useApproveVerification } from "../model/useApproveVerification";

interface ApproveVerificationButtonProps {
  verificationId: string;
}

function addYearsMinusOneDay(years: number): string {
  const today = new Date();
  const year = today.getFullYear() + years;
  const month = today.getMonth();
  const day = today.getDate();
  const lastDay = new Date(year, month + 1, 0).getDate();
  const anniversary = new Date(year, month, Math.min(day, lastDay));
  anniversary.setDate(anniversary.getDate() - 1);
  const yyyy = anniversary.getFullYear();
  const mm = String(anniversary.getMonth() + 1).padStart(2, "0");
  const dd = String(anniversary.getDate()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}`;
}

function formatDate(value: string): string {
  const [year, month, day] = value.split("-");
  return `${day}.${month}.${year}`;
}

export function ApproveVerificationButton({
  verificationId,
}: ApproveVerificationButtonProps) {
  const [durationYears, setDurationYears] = useState("2");
  const [manualValidUntil, setManualValidUntil] = useState("");
  const preview = useMemo(() => {
    const years = Number(durationYears);
    return Number.isInteger(years) && years >= 1 && years <= 100
      ? addYearsMinusOneDay(years)
      : "";
  }, [durationYears]);

  const queryClient = useQueryClient();

  const { mutate, isPending, error } = useApproveVerification({
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["verifications", verificationId],
      });
    },
  });

  const years = Number(durationYears);
  const validYears = Number.isInteger(years) && years >= 1 && years <= 100;

  return (
    <Stack spacing={1.5}>
      <Typography variant="subtitle1">Признать СИ пригодным</Typography>
      {error && <Alert severity="error">{error.message}</Alert>}
      <TextField
        label="Срок действия, лет"
        type="number"
        value={durationYears}
        onChange={(event) => {
          setDurationYears(event.target.value);
          setManualValidUntil("");
        }}
        inputProps={{ min: 1, max: 100, step: 1 }}
        sx={{ maxWidth: 220 }}
      />
      {preview && (
        <Typography variant="body2" color="text.secondary">
          Предварительная дата по текущей локальной дате: {formatDate(preview)}.
          Сервер пересчитает её по моменту принятия решения.
        </Typography>
      )}
      <TextField
        label="Или указать дату вручную"
        type="date"
        value={manualValidUntil}
        onChange={(event) => setManualValidUntil(event.target.value)}
        slotProps={{ inputLabel: { shrink: true } }}
        sx={{ maxWidth: 320 }}
      />
      <Button
        variant="contained"
        color="success"
        disabled={isPending || !validYears}
        onClick={() =>
          mutate({
            verificationId,
            durationYears: years,
            timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
            ...(manualValidUntil ? { validUntil: manualValidUntil } : {}),
          })
        }
        sx={{ alignSelf: "flex-start" }}
      >
        {isPending ? "Сохраняем решение..." : "Подтвердить пригодность"}
      </Button>
    </Stack>
  );
}
