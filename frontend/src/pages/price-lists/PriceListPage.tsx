import { Stack, Typography } from "@mui/material";
import { useParams } from "react-router";

import { usePriceList } from "../../features/price-lists/model/usePriceList";

export function PriceListPage() {
  const { priceListId } = useParams<{ priceListId: string }>();
  const { data, error, isLoading } = usePriceList(priceListId ?? "");

  if (isLoading) {
    return <Typography>Loading...</Typography>;
  }

  if (error) {
    return <Typography>Failed to load price list.</Typography>;
  }

  if (!data) {
    return null;
  }

  return (
    <Stack spacing={2}>
      <Typography variant="h5">Price list</Typography>
      <Typography>Name: {data.name}</Typography>
      <Typography>Type: {data.priceListType}</Typography>
      <Typography>Currency: {data.currency}</Typography>
      {data.description && <Typography>Description: {data.description}</Typography>}
      {data.validFrom && <Typography>Valid from: {data.validFrom}</Typography>}
      {data.validTo && <Typography>Valid to: {data.validTo}</Typography>}
      <Typography>Active: {data.isActive ? "Yes" : "No"}</Typography>
      <Typography>Archived: {data.archived ? "Yes" : "No"}</Typography>
    </Stack>
  );
}
