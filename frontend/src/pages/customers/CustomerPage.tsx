import { Stack, Typography } from "@mui/material";
import { useParams } from "react-router";

import { useCustomer } from "../../features/customers/model/useCustomer";

export function CustomerPage() {
  const { customerId } = useParams<{ customerId: string }>();
  const { data, error, isLoading } = useCustomer(customerId ?? "");

  if (isLoading) {
    return <Typography>Loading...</Typography>;
  }

  if (error) {
    return <Typography>Failed to load customer.</Typography>;
  }

  if (!data) {
    return null;
  }

  return (
    <Stack spacing={2}>
      <Typography variant="h5">{data.name}</Typography>

      {data.contactPerson && (
        <Typography color="text.secondary">
          {data.contactPerson}
        </Typography>
      )}

      {data.phone && <Typography>{data.phone}</Typography>}
      {data.email && <Typography>{data.email}</Typography>}
      {data.comment && <Typography>{data.comment}</Typography>}

      <Typography>Discount: {data.discountPercent}%</Typography>

      {data.archived && (
        <Typography color="text.secondary">Archived</Typography>
      )}
    </Stack>
  );
}
