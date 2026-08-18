import { useMutation, useQueryClient } from "@tanstack/react-query";

import { login } from "../api/login";
import type { AuthenticatedUser } from "./types";

type LoginVariables = {
  username: string;
  password: string;
};

export function useLogin() {
  const queryClient = useQueryClient();

  return useMutation<AuthenticatedUser, Error, LoginVariables>({
    mutationFn: login,
    onSuccess: (user) => {
      queryClient.setQueryData(["current-user"], user);
    },
  });
}
