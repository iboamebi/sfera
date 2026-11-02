import { Button } from "@mui/material";
import { useQueryClient } from "@tanstack/react-query";

import { useStartVerification } from "../model/useStartVerification";

interface StartVerificationButtonProps {
  verificationId: string;
}

export function StartVerificationButton({
  verificationId,
}: StartVerificationButtonProps) {
  const queryClient = useQueryClient();

  const { mutate, isPending } = useStartVerification({
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["verifications", verificationId],
      });
    },
  });

  return (
    <Button
      variant="contained"
      disabled={isPending}
      onClick={() => mutate(verificationId)}
    >
      {isPending ? "Starting..." : "Start verification"}
    </Button>
  );
}
