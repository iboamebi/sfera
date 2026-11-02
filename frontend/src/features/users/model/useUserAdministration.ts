import { useMutation, useQueryClient } from "@tanstack/react-query";

import {
  archiveUser,
  changeUserRole,
  createUser,
  restoreUser,
  setUserActive,
} from "../api/userAdministration";
import type { UserRole } from "./types";

export function useUserAdministration() {
  const queryClient = useQueryClient();

  const refreshUsers = () =>
    queryClient.invalidateQueries({ queryKey: ["users"] });

  const create = useMutation({
    mutationFn: ({ username, role }: { username: string; role: UserRole }) =>
      createUser(username, role),
    onSuccess: refreshUsers,
  });

  const changeRole = useMutation({
    mutationFn: ({ userId, role }: { userId: string; role: UserRole }) =>
      changeUserRole(userId, role),
    onSuccess: refreshUsers,
  });

  const changeStatus = useMutation({
    mutationFn: ({ userId, isActive }: { userId: string; isActive: boolean }) =>
      setUserActive(userId, isActive),
    onSuccess: refreshUsers,
  });

  const archive = useMutation({
    mutationFn: archiveUser,
    onSuccess: refreshUsers,
  });

  const restore = useMutation({
    mutationFn: restoreUser,
    onSuccess: refreshUsers,
  });

  return { create, changeRole, changeStatus, archive, restore };
}
