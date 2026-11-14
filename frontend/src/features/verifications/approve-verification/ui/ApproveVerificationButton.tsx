import { useState } from "react";

import { Alert, Button, Stack, TextField, Typography } from "@mui/material";
import { useQueryClient } from "@tanstack/react-query";

import { useApproveVerification } from "../model/useApproveVerification";

interface ApproveVerificationButtonProps {
  verificationId: string;
}

export function ApproveVerificationButton({
  verificationId,
}: ApproveVerificationButtonProps) {
  const [validUntil, setValidUntil] = useState("");

  const queryClient = useQueryClient();

  const { mutate, isPending, error } = useApproveVerification({
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["verifications", verificationId],
      });
    },
  });

  return (
    <Stack spacing={1.5}>
      <Typography variant="subtitle1">Признать СИ пригодным</Typography>
      {error && <Alert severity="error">{error.message}</Alert>}
      <TextField
        label="Действительно до"
        type="date"
        value={validUntil}
        onChange={(event) => setValidUntil(event.target.value)}
        slotProps={{
          inputLabel: {
            shrink: true,
          },
        }}
        sx={{ maxWidth: 320 }}
      />
      <Button
        variant="contained"
        color="success"
        disabled={isPending || !validUntil}
        onClick={() =>
          mutate({
            verificationId,
            validUntil,
          })
        }
        sx={{ alignSelf: "flex-start" }}
      >
        {isPending ? "Сохраняем решение..." : "Подтвердить пригодность"}
      </Button>
    </Stack>
  );
}
