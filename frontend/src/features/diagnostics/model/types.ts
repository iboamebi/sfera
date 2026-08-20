export interface DiagnosticRead {
  id: string;
  orderItemId: string;
  conclusion: string | null;
  recommendation: string | null;
}
