import { http } from "../../../shared/api/http";

export async function logout(): Promise<void> {
  await http.post("/auth/logout");
}
