import { http } from "../../../shared/api/http";
import type { VerificationRead } from "../model/types";
import { mapVerification } from "./verificationMapper";
import type { VerificationApiDto } from "./types";

export async function getVerification(
  verificationId: string,
): Promise<VerificationRead> {
  const response = await http.get<VerificationApiDto>(
    `/verifications/${verificationId}`,
  );

  return mapVerification(response.data);
}
