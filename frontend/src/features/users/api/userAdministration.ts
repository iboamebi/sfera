import { http } from "../../../shared/api/http";
import type {
  UserCreateInput,
  UserCreated,
  UserProfileInput,
  UserRead,
  UserRole,
} from "../model/types";
import { mapCreatedUser, mapUser } from "./userMapper";
import type {
  UserActiveApiRequest,
  UserApiDto,
  UserCreateApiRequest,
  UserCreatedApiDto,
  UserProfileApiRequest,
  UserRoleApiRequest,
} from "./types";

export async function getUsers(includeArchived = false): Promise<UserRead[]> {
  const response = await http.get<UserApiDto[]>("/users/", {
    params: { include_archived: includeArchived },
  });

  return response.data.map(mapUser);
}

export async function createUser(data: UserCreateInput): Promise<UserCreated> {
  const request: UserCreateApiRequest = {
    username: data.username,
    full_name: data.fullName,
    phone: data.phone.trim() || null,
    position: data.position.trim() || null,
    role: data.role,
  };
  const response = await http.post<UserCreatedApiDto>("/users/", request);

  return mapCreatedUser(response.data);
}

export async function updateUserProfile(
  userId: string,
  data: UserProfileInput,
): Promise<UserRead> {
  const request: UserProfileApiRequest = {
    full_name: data.fullName,
    phone: data.phone.trim() || null,
    position: data.position.trim() || null,
  };
  const response = await http.patch<UserApiDto>(
    `/users/${userId}/profile`,
    request,
  );

  return mapUser(response.data);
}

export async function resetUserPassword(userId: string): Promise<UserCreated> {
  const response = await http.post<UserCreatedApiDto>(
    `/users/${userId}/reset-password`,
  );

  return mapCreatedUser(response.data);
}

export async function changeUserRole(
  userId: string,
  role: UserRole,
): Promise<UserRead> {
  const request: UserRoleApiRequest = { role };
  const response = await http.patch<UserApiDto>(`/users/${userId}/role`, request);

  return mapUser(response.data);
}

export async function setUserActive(
  userId: string,
  isActive: boolean,
): Promise<UserRead> {
  const request: UserActiveApiRequest = { is_active: isActive };
  const response = await http.patch<UserApiDto>(
    `/users/${userId}/status`,
    request,
  );

  return mapUser(response.data);
}

export async function archiveUser(userId: string): Promise<UserRead> {
  const response = await http.post<UserApiDto>(`/users/${userId}/archive`);

  return mapUser(response.data);
}

export async function restoreUser(userId: string): Promise<UserRead> {
  const response = await http.post<UserApiDto>(`/users/${userId}/restore`);

  return mapUser(response.data);
}
