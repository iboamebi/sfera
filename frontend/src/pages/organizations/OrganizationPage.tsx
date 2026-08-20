import { Stack, Typography } from "@mui/material";
import { useParams } from "react-router";

import { useOrganization } from "../../features/organizations/model/useOrganization";

export function OrganizationPage() {
  const { organizationId } = useParams<{ organizationId: string }>();
  const { data, error, isLoading } = useOrganization(organizationId ?? "");

  if (isLoading) {
    return <Typography>Loading...</Typography>;
  }

  if (error) {
    return <Typography>Failed to load organization.</Typography>;
  }

  if (!data) {
    return null;
  }

  return (
    <Stack spacing={2}>
      <Typography variant="h5">{data.name}</Typography>
      {data.shortName && (
        <Typography color="text.secondary">{data.shortName}</Typography>
      )}
      {data.inn && <Typography>INN: {data.inn}</Typography>}
      {data.kpp && <Typography>KPP: {data.kpp}</Typography>}
      {data.ogrn && <Typography>OGRN: {data.ogrn}</Typography>}
      {data.address && <Typography>{data.address}</Typography>}
      {data.phone && <Typography>{data.phone}</Typography>}
      {data.email && <Typography>{data.email}</Typography>}
      {data.website && <Typography>{data.website}</Typography>}
      {data.comment && <Typography>{data.comment}</Typography>}
    </Stack>
  );
}
