import { Stack, Typography } from "@mui/material";
import { Link } from "react-router";

import { useMaterials } from "../../features/materials/model/useMaterials";

export function MaterialsPage() {
  const { data: materials, isLoading, error } = useMaterials();

  if (isLoading) {
    return <Typography>Loading materials...</Typography>;
  }

  if (error) {
    return <Typography>Failed to load materials.</Typography>;
  }

  if (!materials || materials.length === 0) {
    return <Typography>No materials found.</Typography>;
  }

  return (
    <Stack spacing={2}>
      {materials.map((material) => (
        <Stack key={material.id} spacing={0.5}>
          <Typography variant="h6">
            <Link to={`/materials/${material.id}`}>{material.name}</Link>
          </Typography>
          {material.article && (
            <Typography color="text.secondary">{material.article}</Typography>
          )}
          <Typography>Unit: {material.unit}</Typography>
          {material.description && <Typography>{material.description}</Typography>}
        </Stack>
      ))}
    </Stack>
  );
}
