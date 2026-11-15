export type VerificationStatus = "CREATED" | "IN_PROGRESS" | "DECIDED" | "CANCELLED";

export type VerificationType = "PRIMARY" | "PERIODIC" | "AFTER_REPAIR";

export type VerificationResult = "SUITABLE" | "UNSUITABLE";

export interface VerificationRead {
  id: string;
  orderItemId: string;
  instrumentId: string | null;
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
  cancellationReason: string | null;
  archived: boolean;
}

export interface VerificationListRead {
  id: string;
  orderItemId: string;
  orderId: string;
  orderNumber: string;
  customerId: string;
  customerName: string;
  instrumentId: string | null;
  instrumentName: string | null;
  instrumentTypeId: string | null;
  instrumentTypeName: string | null;
  serialNumber: string | null;
  verificationDate: string;
  verificationType: VerificationType;
  status: VerificationStatus;
  result: VerificationResult | null;
  validUntil: string | null;
  createdAt: string;
  startedAt: string | null;
  decisionAt: string | null;
  archived: boolean;
}
