import { http } from "../../../shared/api/http";
import type { VerificationListRead } from "../model/types";
import { mapVerificationList } from "./verificationListMapper";
import type { VerificationListApiDto } from "./types";

export async function getVerifications(): Promise<VerificationListRead[]> {
  const response = await http.get<VerificationListApiDto[]>("/verifications/");

  return response.data.map(mapVerificationList);
}
