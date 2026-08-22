import { useState } from "react";

import { Button, Stack, TextField } from "@mui/material";
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

  const { mutate, isPending } = useRejectVerification({
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["verifications", verificationId],
      });
    },
  });

  return (
    <Stack spacing={1}>
      <TextField
        label="Unsuitable reason"
        value={reason}
        onChange={(event) => setReason(event.target.value)}
      />

      <Button
        variant="outlined"
        disabled={isPending || !reason}
        onClick={() =>
          mutate({
            verificationId,
            reason,
          })
        }
      >
        {isPending ? "Rejecting..." : "Reject"}
      </Button>
    </Stack>
  );
}
