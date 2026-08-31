import { Stack, Typography } from "@mui/material";
import { useParams } from "react-router";

import { useInstrumentType } from "../../features/instrument-type/model/useInstrumentType";

export function InstrumentTypePage() {
  const { instrumentTypeId } = useParams<{ instrumentTypeId: string }>();
  const { data, error, isLoading } = useInstrumentType(
    instrumentTypeId ?? "",
  );

  if (isLoading) {
    return <Typography>Loading...</Typography>;
  }

  if (error) {
    return <Typography>Failed to load instrument type.</Typography>;
  }

  if (!data) {
    return null;
  }

  return (
    <Stack spacing={2}>
      <Typography variant="h5">Наименование СИ: {data.name}</Typography>

      {data.measurementType && (
        <Typography>Тип СИ: {data.measurementType}</Typography>
      )}

      {data.model && (
        <Typography color="text.secondary">
          Модификация: {data.model}
        </Typography>
      )}

      {data.manufacturer && (
        <Typography color="text.secondary">
          Manufacturer: {data.manufacturer}
        </Typography>
      )}

      {data.accuracyClass && (
        <Typography>Accuracy class: {data.accuracyClass}</Typography>
      )}

      {data.verificationIntervalMonths !== null && (
        <Typography>
          Verification interval: {data.verificationIntervalMonths} months
        </Typography>
      )}

      {data.description && <Typography>{data.description}</Typography>}

      {data.archived && (
        <Typography color="text.secondary">Archived</Typography>
      )}
    </Stack>
  );
}
