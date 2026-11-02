import { Alert, Button, Stack } from "@mui/material";
import { useQueryClient } from "@tanstack/react-query";

import { useStartVerification } from "../model/useStartVerification";

interface StartVerificationButtonProps {
  verificationId: string;
}

export function StartVerificationButton({
  verificationId,
}: StartVerificationButtonProps) {
  const queryClient = useQueryClient();

  const { mutate, isPending, error } = useStartVerification({
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["verifications", verificationId],
      });
    },
  });

  return (
    <Stack spacing={1}>
      {error && <Alert severity="error">{error.message}</Alert>}
      <Button
        variant="contained"
        disabled={isPending}
        onClick={() => mutate(verificationId)}
      >
        {isPending ? "Starting..." : "Start verification"}
      </Button>
    </Stack>
  );
}
