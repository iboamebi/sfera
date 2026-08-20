import type { DiagnosticRead } from "../model/types";
import type { DiagnosticApiDto } from "./types";

export function mapDiagnostic(dto: DiagnosticApiDto): DiagnosticRead {
  return {
    id: dto.id,
    orderItemId: dto.order_item_id,
    conclusion: dto.conclusion,
    recommendation: dto.recommendation,
  };
}
