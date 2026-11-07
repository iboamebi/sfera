import { Button, Stack, Typography } from "@mui/material";
import { Link, useParams } from "react-router";

import { useCustomer } from "../../features/customers/model/useCustomer";
import { useCustomerSites } from "../../features/sites/model/useCustomerSites";

export function CustomerPage() {
  const { customerId } = useParams<{ customerId: string }>();
  const { data, error, isLoading } = useCustomer(customerId ?? "");
  const {
    data: sites,
    error: sitesError,
    isLoading: sitesLoading,
  } = useCustomerSites(customerId ?? "");

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
    <Stack spacing={3}>
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

      <Stack spacing={2}>
        <Stack
          direction="row"
          spacing={2}
          sx={{
            alignItems: { xs: "stretch", sm: "center" },
            justifyContent: "space-between",
            flexWrap: "wrap",
          }}
        >
          <Typography variant="h6">Объекты</Typography>
          <Button
            component={Link}
            to={`/customers/${data.id}/sites/new`}
            variant="contained"
          >
            Добавить объект
          </Button>
        </Stack>

        {sitesLoading && <Typography>Загрузка объектов...</Typography>}

        {sitesError && (
          <Typography>Не удалось загрузить объекты.</Typography>
        )}

        {!sitesLoading && !sitesError && (!sites || sites.length === 0) && (
          <Typography color="text.secondary">
            Объекты пока не созданы.
          </Typography>
        )}

        {!sitesLoading && !sitesError && sites && sites.length > 0 && (
          <Stack spacing={1.5}>
            {sites.map((site) => (
              <Stack key={site.id} spacing={0.5}>
                <Typography variant="subtitle1">{site.name}</Typography>
                <Typography color="text.secondary">{site.address}</Typography>
                {site.archived && (
                  <Typography color="text.secondary">В архиве</Typography>
                )}
              </Stack>
            ))}
          </Stack>
        )}
      </Stack>
    </Stack>
  );
}
