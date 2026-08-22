import { ApproveVerificationButton } from "../../features/verifications/approve-verification/ui/ApproveVerificationButton";
import { RejectVerificationButton } from "../../features/verifications/reject-verification/ui/RejectVerificationButton";
import { Stack, Typography } from "@mui/material";
import { useParams } from "react-router";

import { useVerification } from "../../features/verifications/model/useVerification";

export function VerificationPage() {
  const { verificationId } = useParams<{ verificationId: string }>();
  const { data, error, isLoading } = useVerification(verificationId ?? "");

  if (isLoading) {
    return <Typography>Loading...</Typography>;
  }

  if (error) {
    return <Typography>Failed to load verification.</Typography>;
  }

  if (!data) {
    return null;
  }

  return (
    <Stack spacing={2}>
      <Typography variant="h5">Verification</Typography>
      <Typography>Order item: {data.orderItemId}</Typography>
      <Typography>Verification date: {data.verificationDate}</Typography>
      {data.validUntil && <Typography>Valid until: {data.validUntil}</Typography>}
      <Typography>Result: {data.result}</Typography>
      {data.unsuitableReason && (
        <Typography>Unsuitable reason: {data.unsuitableReason}</Typography>
      )}
      {data.methodology && <Typography>Methodology: {data.methodology}</Typography>}
      <ApproveVerificationButton verificationId={data.id} />
      <RejectVerificationButton verificationId={data.id} />
      <Typography>Status: {data.archived ? "Archived" : "Active"}</Typography>
    </Stack>
  );
}
