import { useEffect, useState } from "react";

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
  currentUnsuitableReason: string | null;
}

export function CorrectVerificationDecisionForm({
  verificationId,
  currentResult,
  currentUnsuitableReason,
}: CorrectVerificationDecisionFormProps) {
  const [result, setResult] = useState<VerificationResult>(currentResult);
  const [unsuitableReason, setUnsuitableReason] = useState(
    currentUnsuitableReason ?? "",
  );
  const [reason, setReason] = useState("");
  const queryClient = useQueryClient();

  useEffect(() => {
    setResult(currentResult);
    setUnsuitableReason(currentUnsuitableReason ?? "");
  }, [currentResult, currentUnsuitableReason]);

  const { mutate, isPending, error } = useCorrectVerificationDecision({
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["verifications", verificationId],
      });
    },
  });

  const validDecision =
    result === "UNSUITABLE" && Boolean(unsuitableReason.trim());
  const hasChanges =
    currentResult === "SUITABLE" &&
    result === "UNSUITABLE" &&
    unsuitableReason.trim() !== (currentUnsuitableReason ?? "").trim();

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
        <MenuItem value="SUITABLE" disabled={currentResult === "UNSUITABLE"}>Пригодно</MenuItem>
        <MenuItem value="UNSUITABLE">Непригодно</MenuItem>
      </TextField>
      {currentResult === "UNSUITABLE" && (
        <Alert severity="info">
          Для положительного результата необходимо создать новую поверку.
        </Alert>
      )}
      {result === "SUITABLE" ? (
        <Alert severity="info">
          Для изменения результата на «Пригодно» необходимо создать новую поверку.
        </Alert>
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
        disabled={
          currentResult !== "SUITABLE" ||
          result !== "UNSUITABLE" ||
          !validDecision ||
          !hasChanges ||
          !reason.trim() ||
          isPending
        }
        onClick={() =>
          mutate({
            verificationId,
            result,
            unsuitableReason: unsuitableReason.trim(),
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
