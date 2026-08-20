import { Stack, Typography } from "@mui/material";
import { useParams } from "react-router";

import { useDiagnostic } from "../../features/diagnostics/model/useDiagnostic";

export function DiagnosticPage() {
  const { diagnosticId } = useParams<{ diagnosticId: string }>();
  const { data, error, isLoading } = useDiagnostic(diagnosticId ?? "");

  if (isLoading) {
    return <Typography>Loading...</Typography>;
  }

  if (error) {
    return <Typography>Failed to load diagnostic.</Typography>;
  }

  if (!data) {
    return null;
  }

  return (
    <Stack spacing={2}>
      <Typography variant="h5">Diagnostic</Typography>
      <Typography>Order item: {data.orderItemId}</Typography>
      {data.conclusion && <Typography>Conclusion: {data.conclusion}</Typography>}
      {data.recommendation && (
        <Typography>Recommendation: {data.recommendation}</Typography>
      )}
    </Stack>
  );
}
