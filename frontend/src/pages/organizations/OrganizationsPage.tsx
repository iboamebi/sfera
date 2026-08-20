import { Stack, Typography } from "@mui/material";
import { Link } from "react-router";

import { useOrganizations } from "../../features/organizations/model/useOrganizations";

export function OrganizationsPage() {
  const { data: organizations, isLoading, error } = useOrganizations();

  if (isLoading) {
    return <Typography>Loading organizations...</Typography>;
  }

  if (error) {
    return <Typography>Failed to load organizations.</Typography>;
  }

  if (!organizations || organizations.length === 0) {
    return <Typography>No organizations found.</Typography>;
  }

  return (
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
          {organization.address && <Typography>{organization.address}</Typography>}
          {organization.phone && <Typography>{organization.phone}</Typography>}
          {organization.email && <Typography>{organization.email}</Typography>}
        </Stack>
      ))}
    </Stack>
  );
}
