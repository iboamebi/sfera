import {
  Button,
  Chip,
  Stack,
  Typography,
} from "@mui/material";

import type {
  OrderSortCriterion,
  OrderSortField,
} from "../model/orderSorting";

interface OrderSortControlsProps {
  criteria: OrderSortCriterion[];
  onChange: (criteria: OrderSortCriterion[]) => void;
}

const sortFields: Array<{
  field: OrderSortField;
  label: string;
}> = [
  { field: "number", label: "Номер" },
  { field: "createdAt", label: "Дата" },
  { field: "customerName", label: "Клиент" },
  { field: "status", label: "Статус" },
];

/** Controls multiple order sorting criteria and their priority. */
export function OrderSortControls({
  criteria,
  onChange,
}: OrderSortControlsProps) {
  const handleFieldClick = (field: OrderSortField) => {
    const existingIndex = criteria.findIndex(
      (criterion) => criterion.field === field,
    );

    if (existingIndex === -1) {
      onChange([
        ...criteria,
        {
          field,
          direction: "asc",
        },
      ]);
      return;
    }

    onChange(
      criteria.map((criterion, index) =>
        index === existingIndex
          ? {
              ...criterion,
              direction:
                criterion.direction === "asc"
                  ? "desc"
                  : "asc",
            }
          : criterion,
      ),
    );
  };

  const handleDelete = (field: OrderSortField) => {
    onChange(
      criteria.filter(
        (criterion) => criterion.field !== field,
      ),
    );
  };

  return (
    <Stack spacing={1}>
      <Typography variant="subtitle2">
        Сортировка
      </Typography>

      <Stack
        direction="row"
        spacing={1}
        sx={{ flexWrap: "wrap" }}
      >
        {sortFields.map(({ field, label }) => {
          const criterion = criteria.find(
            (item) => item.field === field,
          );

          return (
            <Button
              key={field}
              size="small"
              variant={criterion ? "contained" : "outlined"}
              onClick={() => handleFieldClick(field)}
            >
              {label}
              {criterion &&
                ` ${criterion.direction === "asc" ? "↑" : "↓"}`}
            </Button>
          );
        })}
      </Stack>

      {criteria.length > 0 && (
        <Stack
          direction="row"
          spacing={1}
          sx={{ flexWrap: "wrap" }}
        >
          {criteria.map((criterion, index) => {
            const label =
              sortFields.find(
                (field) => field.field === criterion.field,
              )?.label ?? criterion.field;

            return (
              <Chip
                key={criterion.field}
                label={`${index + 1}. ${label} ${
                  criterion.direction === "asc" ? "↑" : "↓"
                }`}
                size="small"
                onDelete={() => handleDelete(criterion.field)}
              />
            );
          })}
        </Stack>
      )}
    </Stack>
  );
}
