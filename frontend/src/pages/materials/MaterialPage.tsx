import { Stack, Typography } from "@mui/material";
import { useParams } from "react-router";

import { useMaterial } from "../../features/materials/model/useMaterial";

export function MaterialPage() {
  const { materialId } = useParams<{ materialId: string }>();
  const { data, error, isLoading } = useMaterial(materialId ?? "");

  if (isLoading) {
    return <Typography>Loading...</Typography>;
  }

  if (error) {
    return <Typography>Failed to load material.</Typography>;
  }

  if (!data) {
    return null;
  }

  return (
    <Stack spacing={2}>
      <Typography variant="h5">{data.name}</Typography>
      {data.article && (
        <Typography color="text.secondary">{data.article}</Typography>
      )}
      <Typography>Unit: {data.unit}</Typography>
      {data.description && <Typography>{data.description}</Typography>}
      <Typography>
        Status: {data.archived ? "Archived" : "Active"}
      </Typography>
    </Stack>
  );
}
