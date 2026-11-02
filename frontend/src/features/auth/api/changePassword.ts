import { http } from "../../../shared/api/http";

interface ChangePasswordRequest {
  currentPassword: string;
  newPassword: string;
}

export async function changePassword(
  data: ChangePasswordRequest,
): Promise<void> {
  await http.post("/auth/change-password", {
    current_password: data.currentPassword,
    new_password: data.newPassword,
  });
}
