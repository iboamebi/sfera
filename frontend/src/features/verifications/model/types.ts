export interface VerificationRead {
  id: string;
  orderItemId: string;
  verificationDate: string;
  validUntil: string | null;
  result: string;
  unsuitableReason: string | null;
  methodology: string | null;
  archived: boolean;
}
