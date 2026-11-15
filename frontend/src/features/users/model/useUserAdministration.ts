import { useMutation, useQueryClient } from "@tanstack/react-query";

import {
  archiveUser,
  changeUserRole,
  createUser,
  restoreUser,
  resetUserPassword,
  setUserActive,
  updateUserProfile,
} from "../api/userAdministration";
import type { UserCreateInput, UserProfileInput, UserRole } from "./types";

export function useUserAdministration() {
  const queryClient = useQueryClient();

  const refreshUsers = () =>
    queryClient.invalidateQueries({ queryKey: ["users"] });

  const create = useMutation({
    mutationFn: (data: UserCreateInput) => createUser(data),
    onSuccess: refreshUsers,
  });

  const updateProfile = useMutation({
    mutationFn: ({ userId, data }: { userId: string; data: UserProfileInput }) =>
      updateUserProfile(userId, data),
    onSuccess: refreshUsers,
  });

  const resetPassword = useMutation({
    mutationFn: resetUserPassword,
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

  return {
    create,
    updateProfile,
    resetPassword,
    changeRole,
    changeStatus,
    archive,
    restore,
  };
}
