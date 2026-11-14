import { useEffect, useState } from "react";

import { Alert, Button, Stack, TextField, Typography } from "@mui/material";
import { useQueryClient } from "@tanstack/react-query";

import { useCorrectVerificationValidUntil } from "../model/useCorrectVerificationValidUntil";

interface CorrectVerificationValidUntilFormProps {
  verificationId: string;
  currentValidUntil: string;
}

export function CorrectVerificationValidUntilForm({
  verificationId,
  currentValidUntil,
}: CorrectVerificationValidUntilFormProps) {
  const [validUntil, setValidUntil] = useState(currentValidUntil);
  const [reason, setReason] = useState("");
  const queryClient = useQueryClient();
  const { mutate, isPending, error } = useCorrectVerificationValidUntil({
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["verifications", verificationId],
      });
    },
  });

  useEffect(() => {
    setValidUntil(currentValidUntil);
  }, [currentValidUntil]);

  return (
    <Stack spacing={1.5}>
      <Typography variant="subtitle1">Исправить срок действия</Typography>
      {error && <Alert severity="error">{error.message}</Alert>}
      <TextField
        label="Правильная дата «Действительна до»"
        type="date"
        value={validUntil}
        onChange={(event) => setValidUntil(event.target.value)}
        slotProps={{ inputLabel: { shrink: true } }}
        sx={{ maxWidth: 320 }}
      />
      <TextField
        label="Причина исправления"
        value={reason}
        onChange={(event) => setReason(event.target.value)}
        multiline
        minRows={2}
        fullWidth
      />
      <Button
        variant="contained"
        disabled={
          isPending ||
          !validUntil ||
          validUntil === currentValidUntil ||
          !reason.trim()
        }
        onClick={() => mutate({ verificationId, validUntil, reason: reason.trim() })}
        sx={{ alignSelf: "flex-start" }}
      >
        {isPending ? "Сохраняем..." : "Сохранить исправление"}
      </Button>
    </Stack>
  );
}
