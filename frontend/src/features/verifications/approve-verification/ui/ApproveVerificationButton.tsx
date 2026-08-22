import { useState } from "react";

import { Button, Stack, TextField } from "@mui/material";
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

  const { mutate, isPending } = useApproveVerification({
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["verifications", verificationId],
      });
    },
  });

  return (
    <Stack spacing={1}>
      <TextField
        label="Valid until"
        type="date"
        value={validUntil}
        onChange={(event) => setValidUntil(event.target.value)}
        slotProps={{
          inputLabel: {
            shrink: true,
          },
        }}
      />

      <Button
        variant="contained"
        disabled={isPending || !validUntil}
        onClick={() =>
          mutate({
            verificationId,
            validUntil,
          })
        }
      >
        {isPending ? "Approving..." : "Approve"}
      </Button>
    </Stack>
  );
}
