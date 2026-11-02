export type VerificationStatus = "CREATED" | "IN_PROGRESS" | "DECIDED";

export type VerificationType = "PRIMARY" | "PERIODIC" | "AFTER_REPAIR";

export type VerificationResult = "SUITABLE" | "UNSUITABLE";

export interface VerificationRead {
  id: string;
  orderItemId: string;
  verificationDate: string;
  validUntil: string | null;
  result: VerificationResult | null;
  unsuitableReason: string | null;
  methodology: string | null;
  createdAt: string;
  startedAt: string | null;
  decisionAt: string | null;
  status: VerificationStatus;
  verificationType: VerificationType;
  archived: boolean;
}
