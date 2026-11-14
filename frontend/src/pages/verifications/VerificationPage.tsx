import {
  Alert,
  Card,
  CardContent,
  Chip,
  Divider,
  Stack,
  Typography,
} from "@mui/material";
import { useParams } from "react-router";

import { ApproveVerificationButton } from "../../features/verifications/approve-verification/ui/ApproveVerificationButton";
import { RejectVerificationButton } from "../../features/verifications/reject-verification/ui/RejectVerificationButton";
import { StartVerificationButton } from "../../features/verifications/start-verification/ui/StartVerificationButton";
import { useVerification } from "../../features/verifications/model/useVerification";
import type {
  VerificationResult,
  VerificationStatus,
  VerificationType,
} from "../../features/verifications/model/types";

const STATUS_LABELS: Record<VerificationStatus, string> = {
  CREATED: "Создана",
  IN_PROGRESS: "В работе",
  DECIDED: "Решение принято",
};

const TYPE_LABELS: Record<VerificationType, string> = {
  PRIMARY: "Первичная",
  PERIODIC: "Периодическая",
  AFTER_REPAIR: "После ремонта",
};

const RESULT_LABELS: Record<VerificationResult, string> = {
  SUITABLE: "Пригодно",
  UNSUITABLE: "Непригодно",
};

function formatDate(value: string | null): string {
  if (!value) return "—";
  const [year, month, day] = value.slice(0, 10).split("-");
  return year && month && day ? `${day}.${month}.${year}` : value;
}

function formatDateTime(value: string | null): string {
  if (!value) return "—";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat("ru-RU", {
    dateStyle: "short",
    timeStyle: "short",
  }).format(date);
}

function getStatusColor(
  status: VerificationStatus,
  result: VerificationResult | null,
): "default" | "info" | "success" | "error" {
  if (status === "CREATED") return "default";
  if (status === "IN_PROGRESS") return "info";
  return result === "SUITABLE" ? "success" : "error";
}

interface DetailRowProps {
  label: string;
  value: string;
}

function DetailRow({ label, value }: DetailRowProps) {
  return (
    <Stack spacing={0.25}>
      <Typography variant="caption" color="text.secondary">
        {label}
      </Typography>
      <Typography variant="body1">{value}</Typography>
    </Stack>
  );
}

export function VerificationPage() {
  const { verificationId } = useParams<{ verificationId: string }>();
  const { data, error, isLoading } = useVerification(verificationId ?? "");

  if (isLoading) {
    return <Typography color="text.secondary">Загрузка поверки...</Typography>;
  }

  if (error) {
    return <Alert severity="error">Не удалось загрузить сведения о поверке.</Alert>;
  }

  if (!data) {
    return <Alert severity="warning">Поверка не найдена.</Alert>;
  }

  const canStart = !data.archived && data.status === "CREATED";
  const canDecide = !data.archived && data.status === "IN_PROGRESS";

  return (
    <Stack spacing={3} sx={{ width: "100%", maxWidth: 960, mx: "auto" }}>
      <Stack spacing={1}>
        <Typography variant="h4">Поверка</Typography>
        <Stack direction="row" spacing={1} sx={{ alignItems: "center", flexWrap: "wrap" }}>
          <Chip
            label={STATUS_LABELS[data.status]}
            color={getStatusColor(data.status, data.result)}
          />
          {data.archived && <Chip label="В архиве" variant="outlined" />}
          {data.result && (
            <Chip
              label={RESULT_LABELS[data.result]}
              color={data.result === "SUITABLE" ? "success" : "error"}
              variant="outlined"
            />
          )}
        </Stack>
      </Stack>

      <Card variant="outlined">
        <CardContent>
          <Stack spacing={2}>
            <Typography variant="h6">Основные сведения</Typography>
            <Divider />
            <DetailRow label="Дата поверки" value={formatDate(data.verificationDate)} />
            <DetailRow label="Вид поверки" value={TYPE_LABELS[data.verificationType]} />
            <DetailRow label="Методика" value={data.methodology || "Не указана"} />
            <DetailRow label="Позиция заказа" value={data.orderItemId} />
          </Stack>
        </CardContent>
      </Card>

      <Card variant="outlined">
        <CardContent>
          <Stack spacing={2}>
            <Typography variant="h6">Результат и сроки</Typography>
            <Divider />
            <DetailRow
              label="Результат"
              value={data.result ? RESULT_LABELS[data.result] : "Решение ещё не принято"}
            />
            <DetailRow label="Действительна до" value={formatDate(data.validUntil)} />
            {data.unsuitableReason && (
              <DetailRow label="Причина непригодности" value={data.unsuitableReason} />
            )}
          </Stack>
        </CardContent>
      </Card>

      <Card variant="outlined">
        <CardContent>
          <Stack spacing={2}>
            <Typography variant="h6">История выполнения</Typography>
            <Divider />
            <DetailRow label="Создана" value={formatDateTime(data.createdAt)} />
            <DetailRow label="Начата" value={formatDateTime(data.startedAt)} />
            <DetailRow label="Решение принято" value={formatDateTime(data.decisionAt)} />
          </Stack>
        </CardContent>
      </Card>

      {(canStart || canDecide) && (
        <Card variant="outlined">
          <CardContent>
            <Stack spacing={2}>
              <Typography variant="h6">Действия</Typography>
              <Divider />
              {canStart && <StartVerificationButton verificationId={data.id} />}
              {canDecide && (
                <Stack spacing={2}>
                  <ApproveVerificationButton verificationId={data.id} />
                  <Divider />
                  <RejectVerificationButton verificationId={data.id} />
                </Stack>
              )}
            </Stack>
          </CardContent>
        </Card>
      )}
    </Stack>
  );
}
