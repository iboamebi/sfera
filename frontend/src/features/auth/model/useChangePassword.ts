import { useMutation, useQueryClient } from "@tanstack/react-query";

import { changePassword } from "../api/changePassword";

interface ChangePasswordVariables {
  currentPassword: string;
  newPassword: string;
}

export function useChangePassword() {
  const queryClient = useQueryClient();

  return useMutation<void, Error, ChangePasswordVariables>({
    mutationFn: changePassword,
    onSuccess: async () => {
      await queryClient.invalidateQueries({
        queryKey: ["auth", "current-user"],
      });
    },
  });
}
