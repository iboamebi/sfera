import { Stack, Typography } from "@mui/material";
import { useParams } from "react-router";

import { useRepair } from "../../features/repairs/model/useRepair";

export function RepairPage() {
  const { repairId } = useParams<{ repairId: string }>();
  const { data, error, isLoading } = useRepair(repairId ?? "");

  if (isLoading) {
    return <Typography>Loading...</Typography>;
  }

  if (error) {
    return <Typography>Failed to load repair.</Typography>;
  }

  if (!data) {
    return null;
  }

  return (
    <Stack spacing={2}>
      <Typography variant="h5">Repair</Typography>
      <Typography>Order item: {data.orderItemId}</Typography>
      <Typography>Status: {data.status}</Typography>
      {data.description && <Typography>Description: {data.description}</Typography>}
      {data.result && <Typography>Result: {data.result}</Typography>}
    </Stack>
  );
}
