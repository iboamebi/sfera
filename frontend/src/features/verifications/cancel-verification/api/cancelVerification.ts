import { http } from "../../../../shared/api/http";
import { mapVerification } from "../../api/verificationMapper";
import type { VerificationApiDto } from "../../api/types";
import type { VerificationRead } from "../../model/types";
export async function cancelVerification(input: { verificationId: string; reason?: string }): Promise<VerificationRead> {
 const response = await http.post<VerificationApiDto>(`/verifications/${input.verificationId}/cancel`, { reason: input.reason });
 return mapVerification(response.data);
}
