import type { OrderRead } from "./types";

export type OrderSortField =
  | "number"
  | "createdAt"
  | "customerName"
  | "status";

export type SortDirection = "asc" | "desc";

export interface OrderSortCriterion {
  field: OrderSortField;
  direction: SortDirection;
}

/** Sorts orders by multiple criteria in priority order. */
export function sortOrders(
  orders: OrderRead[],
  criteria: OrderSortCriterion[],
): OrderRead[] {
  if (criteria.length === 0) {
    return orders;
  }

  return [...orders].sort((left, right) => {
    for (const criterion of criteria) {
      const comparison = compareByField(
        left,
        right,
        criterion.field,
      );

      if (comparison !== 0) {
        return criterion.direction === "asc"
          ? comparison
          : -comparison;
      }
    }

    return 0;
  });
}

/** Compares two orders by a single supported field. */
function compareByField(
  left: OrderRead,
  right: OrderRead,
  field: OrderSortField,
): number {
  switch (field) {
    case "number":
      return left.number.localeCompare(
        right.number,
        "ru",
        { numeric: true },
      );

    case "createdAt":
      return (
        new Date(left.createdAt).getTime() -
        new Date(right.createdAt).getTime()
      );

    case "customerName":
      return left.customerName.localeCompare(
        right.customerName,
        "ru",
      );

    case "status":
      return left.status.localeCompare(
        right.status,
        "ru",
      );
  }
}
