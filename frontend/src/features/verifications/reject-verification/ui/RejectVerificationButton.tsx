import { useState } from "react";

import { Alert, Button, Stack, TextField, Typography } from "@mui/material";
import { useQueryClient } from "@tanstack/react-query";

import { useRejectVerification } from "../model/useRejectVerification";

interface RejectVerificationButtonProps {
  verificationId: string;
}

export function RejectVerificationButton({
  verificationId,
}: RejectVerificationButtonProps) {
  const [reason, setReason] = useState("");

  const queryClient = useQueryClient();

  const { mutate, isPending, error } = useRejectVerification({
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["verifications", verificationId],
      });
    },
  });

  return (
    <Stack spacing={1.5}>
      <Typography variant="subtitle1">Признать СИ непригодным</Typography>
      {error && <Alert severity="error">{error.message}</Alert>}
      <TextField
        label="Причина непригодности"
        value={reason}
        onChange={(event) => setReason(event.target.value)}
        multiline
        minRows={2}
        fullWidth
      />
      <Button
        variant="outlined"
        color="error"
        disabled={isPending || !reason.trim()}
        onClick={() =>
          mutate({
            verificationId,
            reason,
          })
        }
        sx={{ alignSelf: "flex-start" }}
      >
        {isPending ? "Сохраняем решение..." : "Подтвердить непригодность"}
      </Button>
    </Stack>
  );
}
