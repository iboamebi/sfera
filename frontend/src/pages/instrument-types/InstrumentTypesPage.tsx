import { Stack, Typography } from "@mui/material";

import { useInstrumentTypes } from "../../features/instrument-type/model/useInstrumentTypes";

export function InstrumentTypesPage() {
  const { data: instrumentTypes, isLoading, error } = useInstrumentTypes();

  if (isLoading) {
    return <Typography>Loading instrument types...</Typography>;
  }

  if (error) {
    return <Typography>Failed to load instrument types.</Typography>;
  }

  return (
    <Stack spacing={2}>
      {instrumentTypes?.length === 0 && (
        <Typography>No instrument types.</Typography>
      )}

      {instrumentTypes?.map((instrumentType) => (
        <Stack key={instrumentType.id} spacing={0.5}>
          <Typography variant="h6">{instrumentType.name}</Typography>

          {instrumentType.manufacturer && (
            <Typography color="text.secondary">
              {instrumentType.manufacturer}
            </Typography>
          )}

          {instrumentType.model && (
            <Typography color="text.secondary">
              {instrumentType.model}
            </Typography>
          )}
        </Stack>
      ))}
    </Stack>
  );
}
