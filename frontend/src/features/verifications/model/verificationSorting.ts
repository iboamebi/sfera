import type {
  VerificationListRead,
  VerificationResult,
  VerificationStatus,
  VerificationType,
} from "./types";

export type VerificationSortField =
  | "verificationDate"
  | "orderNumber"
  | "customerName"
  | "instrument"
  | "verificationType"
  | "status"
  | "result"
  | "validUntil";

export type SortDirection = "asc" | "desc";

export interface VerificationSortCriterion {
  field: VerificationSortField;
  direction: SortDirection;
}

const TYPE_LABELS: Record<VerificationType, string> = {
  PRIMARY: "Первичная",
  PERIODIC: "Периодическая",
  AFTER_REPAIR: "После ремонта",
};

const STATUS_LABELS: Record<VerificationStatus, string> = {
  CREATED: "Создана",
  IN_PROGRESS: "В работе",
  DECIDED: "Решение принято",
  CANCELLED: "Отменена",
};

const RESULT_LABELS: Record<VerificationResult, string> = {
  SUITABLE: "Пригодно",
  UNSUITABLE: "Непригодно",
};

/** Sorts verifications by multiple header-selected criteria in priority order. */
export function sortVerifications(
  verifications: VerificationListRead[],
  criteria: VerificationSortCriterion[],
): VerificationListRead[] {
  if (criteria.length === 0) {
    return verifications;
  }

  return [...verifications].sort((left, right) => {
    for (const criterion of criteria) {
      const comparison = compareByField(left, right, criterion.field);

      if (comparison !== 0) {
        if (
          (criterion.field === "result" &&
            (left.result === null || right.result === null)) ||
          (criterion.field === "validUntil" &&
            (left.validUntil === null || right.validUntil === null))
        ) {
          return comparison;
        }

        return criterion.direction === "asc" ? comparison : -comparison;
      }
    }

    return 0;
  });
}

function compareByField(
  left: VerificationListRead,
  right: VerificationListRead,
  field: VerificationSortField,
): number {
  switch (field) {
    case "verificationDate":
      return left.verificationDate.localeCompare(right.verificationDate);

    case "orderNumber":
      return left.orderNumber.localeCompare(right.orderNumber, "ru", {
        numeric: true,
      });

    case "customerName":
      return left.customerName.localeCompare(right.customerName, "ru");

    case "instrument":
      return getInstrumentName(left).localeCompare(
        getInstrumentName(right),
        "ru",
      );

    case "verificationType":
      return TYPE_LABELS[left.verificationType].localeCompare(
        TYPE_LABELS[right.verificationType],
        "ru",
      );

    case "status":
      return STATUS_LABELS[left.status].localeCompare(
        STATUS_LABELS[right.status],
        "ru",
      );

    case "result":
      if (left.result === null) return right.result === null ? 0 : 1;
      if (right.result === null) return -1;
      return RESULT_LABELS[left.result].localeCompare(
        RESULT_LABELS[right.result],
        "ru",
      );

    case "validUntil":
      if (left.validUntil === null) return right.validUntil === null ? 0 : 1;
      if (right.validUntil === null) return -1;
      return left.validUntil.localeCompare(right.validUntil);
  }
}

function getInstrumentName(verification: VerificationListRead): string {
  return [
    verification.instrumentName ?? verification.instrumentTypeName ?? "",
    verification.serialNumber ?? "",
  ].join(" ");
}
