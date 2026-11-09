import { Button, Stack, Typography } from "@mui/material";
import { Link } from "react-router";

import { useOrganizations } from "../../features/organizations/model/useOrganizations";

export function OrganizationsPage() {
  const { data: organizations, isLoading, error } = useOrganizations();

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
        <Typography variant="h4">Организации</Typography>
        <Button component={Link} to="/organizations/new" variant="contained">
          Создать организацию
        </Button>
      </Stack>

      {isLoading && <Typography>Загрузка организаций...</Typography>}

      {error && (
        <Typography color="error">
          Не удалось загрузить организации.
        </Typography>
      )}

      {!isLoading && !error && (!organizations || organizations.length === 0) && (
        <Typography color="text.secondary">
          Организации пока не созданы.
        </Typography>
      )}

      {!isLoading && !error && organizations && organizations.length > 0 && (
        <Stack spacing={2}>
          {organizations.map((organization) => (
            <Stack key={organization.id} spacing={0.5}>
              <Typography variant="h6">
                <Link to={`/organizations/${organization.id}`}>
                  {organization.name}
                </Link>
              </Typography>
              {organization.shortName && (
                <Typography color="text.secondary">
                  {organization.shortName}
                </Typography>
              )}
              {organization.inn && <Typography>ИНН: {organization.inn}</Typography>}
              {organization.address && <Typography>{organization.address}</Typography>}
              {organization.phone && <Typography>{organization.phone}</Typography>}
              {organization.email && <Typography>{organization.email}</Typography>}
            </Stack>
          ))}
        </Stack>
      )}
    </Stack>
  );
}
