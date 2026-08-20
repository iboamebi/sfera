import { useQuery } from "@tanstack/react-query";

import { getVerification } from "../api/getVerification";

export function useVerification(verificationId: string) {
  return useQuery({
    queryKey: ["verifications", verificationId],
    queryFn: () => getVerification(verificationId),
    enabled: Boolean(verificationId),
  });
}
