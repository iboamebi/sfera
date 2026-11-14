import { useState } from "react";

import {
  Alert,
  Button,
  MenuItem,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import { useQueryClient } from "@tanstack/react-query";

import { useCorrectVerificationDecision } from "../model/useCorrectVerificationDecision";
import type { VerificationResult } from "../../model/types";

interface CorrectVerificationDecisionFormProps {
  verificationId: string;
  currentResult: VerificationResult;
  currentValidUntil: string | null;
  currentUnsuitableReason: string | null;
}

export function CorrectVerificationDecisionForm({
  verificationId,
  currentResult,
  currentValidUntil,
  currentUnsuitableReason,
}: CorrectVerificationDecisionFormProps) {
  const [result, setResult] = useState<VerificationResult>(currentResult);
  const [validUntil, setValidUntil] = useState(currentValidUntil ?? "");
  const [unsuitableReason, setUnsuitableReason] = useState(
    currentUnsuitableReason ?? "",
  );
  const [reason, setReason] = useState("");
  const queryClient = useQueryClient();

  const { mutate, isPending, error } = useCorrectVerificationDecision({
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["verifications", verificationId],
      });
    },
  });

  const validDecision =
    result === "SUITABLE" ? Boolean(validUntil) : Boolean(unsuitableReason.trim());

  return (
    <Stack spacing={1.5}>
      <Typography variant="subtitle1">Исправить решение о результате</Typography>
      {error && <Alert severity="error">{error.message}</Alert>}
      <TextField
        select
        label="Правильный результат"
        value={result}
        onChange={(event) =>
          setResult(event.target.value as VerificationResult)
        }
        sx={{ maxWidth: 320 }}
      >
        <MenuItem value="SUITABLE">Пригодно</MenuItem>
        <MenuItem value="UNSUITABLE">Непригодно</MenuItem>
      </TextField>
      {result === "SUITABLE" ? (
        <TextField
          label="Действительна до"
          type="date"
          value={validUntil}
          onChange={(event) => setValidUntil(event.target.value)}
          slotProps={{ inputLabel: { shrink: true } }}
          sx={{ maxWidth: 320 }}
        />
      ) : (
        <TextField
          label="Причина непригодности"
          value={unsuitableReason}
          onChange={(event) => setUnsuitableReason(event.target.value)}
          multiline
          minRows={2}
          fullWidth
        />
      )}
      <TextField
        label="Причина исправления решения"
        value={reason}
        onChange={(event) => setReason(event.target.value)}
        multiline
        minRows={2}
        fullWidth
      />
      <Button
        variant="contained"
        disabled={!validDecision || !reason.trim() || isPending}
        onClick={() =>
          mutate({
            verificationId,
            result,
            ...(result === "SUITABLE"
              ? { validUntil }
              : { unsuitableReason: unsuitableReason.trim() }),
            reason: reason.trim(),
          })
        }
        sx={{ alignSelf: "flex-start" }}
      >
        {isPending ? "Сохраняем исправление..." : "Сохранить новое решение"}
      </Button>
    </Stack>
  );
}
