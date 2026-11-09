import { Stack, Typography } from "@mui/material";
import { useParams } from "react-router";

import { ApproveVerificationButton } from "../../features/verifications/approve-verification/ui/ApproveVerificationButton";
import { RejectVerificationButton } from "../../features/verifications/reject-verification/ui/RejectVerificationButton";
import { StartVerificationButton } from "../../features/verifications/start-verification/ui/StartVerificationButton";
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
      <Typography>Verification type: {data.verificationType}</Typography>
      <Typography>Status: {data.status}</Typography>
      <Typography>Created at: {data.createdAt}</Typography>
      {data.startedAt && <Typography>Started at: {data.startedAt}</Typography>}
      {data.decisionAt && <Typography>Decision at: {data.decisionAt}</Typography>}
      {data.validUntil && <Typography>Valid until: {data.validUntil}</Typography>}
      <Typography>Result: {data.result ?? "—"}</Typography>
      {data.unsuitableReason && (
        <Typography>Unsuitable reason: {data.unsuitableReason}</Typography>
      )}
      {data.methodology && <Typography>Methodology: {data.methodology}</Typography>}
      {!data.archived && data.status === "CREATED" && (
        <StartVerificationButton verificationId={data.id} />
      )}
      {!data.archived && data.status === "IN_PROGRESS" && (
        <>
          <ApproveVerificationButton verificationId={data.id} />
          <RejectVerificationButton verificationId={data.id} />
        </>
      )}
      <Typography>Archived: {data.archived ? "Yes" : "No"}</Typography>
    </Stack>
  );
}
