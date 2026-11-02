import type { UserCreated, UserRead } from "../model/types";
import type { UserApiDto, UserCreatedApiDto } from "./types";

export function mapUser(dto: UserApiDto): UserRead {
  return {
    id: dto.id,
    username: dto.username,
    role: dto.role,
    isActive: dto.is_active,
    archived: dto.archived,
    mustChangePassword: dto.must_change_password,
  };
}

export function mapCreatedUser(dto: UserCreatedApiDto): UserCreated {
  return {
    ...mapUser(dto),
    temporaryPassword: dto.temporary_password,
  };
}
