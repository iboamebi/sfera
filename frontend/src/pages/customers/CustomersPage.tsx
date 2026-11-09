import { Button, Stack, Typography } from "@mui/material";
import { Link } from "react-router";

import { useCustomers } from "../../features/customers/model/useCustomers";

export function CustomersPage() {
  const { data: customers, isLoading, error } = useCustomers();

  if (isLoading) {
    return <Typography>Загрузка клиентов...</Typography>;
  }

  if (error) {
    return <Typography>Не удалось загрузить клиентов.</Typography>;
  }

  return (
    <Stack spacing={3}>
      <Stack
        direction="row"
        spacing={2}
        sx={{
          alignItems: { xs: "stretch", sm: "center" },
          justifyContent: "space-between",
          flexWrap: "wrap",
        }}
      >
        <Typography variant="h4">Клиенты</Typography>
        <Button component={Link} to="/customers/new" variant="contained">
          Создать клиента
        </Button>
      </Stack>

      {!customers || customers.length === 0 ? (
        <Typography color="text.secondary">Клиенты пока не созданы.</Typography>
      ) : (
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
                <Typography color="text.secondary">В архиве</Typography>
              )}
            </Stack>
          ))}
        </Stack>
      )}
    </Stack>
  );
}
