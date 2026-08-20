import { Stack, Typography } from "@mui/material";
import { Link } from "react-router";

import { useCustomers } from "../../features/customers/model/useCustomers";

export function CustomersPage() {
  const { data: customers, isLoading, error } = useCustomers();

  if (isLoading) {
    return <Typography>Loading customers...</Typography>;
  }

  if (error) {
    return <Typography>Failed to load customers.</Typography>;
  }

  if (!customers || customers.length === 0) {
    return <Typography>No customers found.</Typography>;
  }

  return (
    <Stack spacing={2}>
      {customers.map((customer) => (
        <Stack key={customer.id} spacing={0.5}>
          <Typography variant="h6">
            <Link to={`/customers/${customer.id}`}>{customer.name}</Link>
          </Typography>
          {customer.contactPerson && (
            <Typography color="text.secondary">
              {customer.contactPerson}
            </Typography>
          )}
          {customer.phone && <Typography>{customer.phone}</Typography>}
          {customer.email && <Typography>{customer.email}</Typography>}
          {customer.archived && (
            <Typography color="text.secondary">Archived</Typography>
          )}
        </Stack>
      ))}
    </Stack>
  );
}
