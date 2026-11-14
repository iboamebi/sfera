import {
  Alert,
  Box,
  Card,
  CardContent,
  Chip,
  Divider,
  Stack,
  Typography,
} from "@mui/material";
import { useParams } from "react-router";

import { useDevice } from "../../features/devices/model/useDevice";
import { useInstrumentType } from "../../features/instrument-type/model/useInstrumentType";
import { ApproveVerificationButton } from "../../features/verifications/approve-verification/ui/ApproveVerificationButton";
import { CorrectVerificationValidUntilForm } from "../../features/verifications/correct-valid-until/ui/CorrectVerificationValidUntilForm";
import { CorrectVerificationDecisionForm } from "../../features/verifications/correct-decision/ui/CorrectVerificationDecisionForm";
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
    <Box sx={{ flex: "1 1 220px", minWidth: 0 }}>
      <Typography variant="caption" color="text.secondary" sx={{ display: "block" }}>
        {label}
      </Typography>
      <Typography variant="body1" sx={{ overflowWrap: "anywhere" }}>
        {value}
      </Typography>
    </Box>
  );
}

interface SectionCardProps {
  title: string;
  children: React.ReactNode;
}

function SectionCard({ title, children }: SectionCardProps) {
  return (
    <Card variant="outlined">
      <CardContent sx={{ p: 2, "&:last-child": { pb: 2 } }}>
        <Stack spacing={1.5}>
          <Typography variant="h6">{title}</Typography>
          <Divider />
          {children}
        </Stack>
      </CardContent>
    </Card>
  );
}

export function VerificationPage() {
  const { verificationId } = useParams<{ verificationId: string }>();
  const { data, error, isLoading } = useVerification(verificationId ?? "");
  const {
    data: instrument,
    error: instrumentError,
    isLoading: instrumentLoading,
  } = useDevice(data?.instrumentId ?? "");
  const {
    data: instrumentType,
    error: instrumentTypeError,
    isLoading: instrumentTypeLoading,
  } = useInstrumentType(instrument?.instrumentTypeId ?? "");

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
  const canCorrectValidity =
    !data.archived &&
    data.status === "DECIDED" &&
    data.result === "SUITABLE" &&
    Boolean(data.validUntil);
  const canCorrectDecision =
    !data.archived &&
    data.status === "DECIDED" &&
    data.result !== null;

  return (
    <Stack spacing={2} sx={{ width: "100%", maxWidth: 1100, mx: "auto" }}>
      <Stack spacing={1}>
        <Typography variant="h4">Поверка</Typography>
        <Stack
          direction="row"
          spacing={1}
          useFlexGap
          sx={{ alignItems: "center", flexWrap: "wrap" }}
        >
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

      <Box
        sx={{
          display: "grid",
          gridTemplateColumns: { xs: "1fr", md: "repeat(2, minmax(0, 1fr))" },
          gap: 2,
          alignItems: "start",
        }}
      >
        <SectionCard title="Средство измерений">
          {instrumentLoading && (
            <Typography color="text.secondary">Загрузка сведений о СИ...</Typography>
          )}
          {instrumentError && (
            <Alert severity="warning">Не удалось загрузить карточку СИ.</Alert>
          )}
          {!instrumentLoading && !instrumentError && !instrument && (
            <Typography color="text.secondary">
              К поверке не привязана карточка СИ.
            </Typography>
          )}
          {instrument && (
            <>
              {instrumentTypeLoading && (
                <Typography color="text.secondary">Загрузка типа СИ...</Typography>
              )}
              {instrumentTypeError && (
                <Alert severity="warning">Не удалось загрузить тип СИ.</Alert>
              )}
              <Stack direction="row" sx={{ flexWrap: "wrap", gap: 2 }}>
                <DetailRow
                  label="Наименование"
                  value={instrument.name || instrumentType?.name || "—"}
                />
                <DetailRow label="Тип СИ" value={instrumentType?.name ?? "—"} />
                <DetailRow label="Заводской номер" value={instrument.serialNumber} />
                <DetailRow label="Регистрационный номер" value={instrument.registryNumber ?? "—"} />
                <DetailRow label="Модификация" value={instrument.modification ?? "—"} />
                <DetailRow label="Год выпуска" value={instrument.manufactureYear?.toString() ?? "—"} />
                <DetailRow label="Инвентарный номер" value={instrument.inventoryNumber ?? "—"} />
              </Stack>
            </>
          )}
        </SectionCard>

        <SectionCard title="Основные сведения">
          <Stack direction="row" sx={{ flexWrap: "wrap", gap: 2 }}>
            <DetailRow label="Дата поверки" value={formatDate(data.verificationDate)} />
            <DetailRow label="Вид поверки" value={TYPE_LABELS[data.verificationType]} />
            <DetailRow label="Методика" value={data.methodology || "Не указана"} />
          </Stack>
        </SectionCard>

        <SectionCard title="Результат и сроки">
          <Stack direction="row" sx={{ flexWrap: "wrap", gap: 2 }}>
            <DetailRow
              label="Результат"
              value={data.result ? RESULT_LABELS[data.result] : "Решение ещё не принято"}
            />
            <DetailRow label="Действительна до" value={formatDate(data.validUntil)} />
            {data.unsuitableReason && (
              <DetailRow label="Причина непригодности" value={data.unsuitableReason} />
            )}
          </Stack>
        </SectionCard>

        <SectionCard title="История выполнения">
          <Stack direction="row" sx={{ flexWrap: "wrap", gap: 2 }}>
            <DetailRow label="Создана" value={formatDateTime(data.createdAt)} />
            <DetailRow label="Начата" value={formatDateTime(data.startedAt)} />
            <DetailRow label="Решение принято" value={formatDateTime(data.decisionAt)} />
          </Stack>
        </SectionCard>

        {(canStart || canDecide || canCorrectValidity || canCorrectDecision) && (
          <SectionCard title="Действия">
            {canStart && <StartVerificationButton verificationId={data.id} />}
            {canDecide && (
              <Stack spacing={1.5}>
                <ApproveVerificationButton verificationId={data.id} />
                <Divider />
                <RejectVerificationButton verificationId={data.id} />
              </Stack>
            )}
            {canCorrectValidity && data.validUntil && (
              <CorrectVerificationValidUntilForm
                verificationId={data.id}
                currentValidUntil={data.validUntil}
              />
            )}
            {canCorrectDecision && data.result && (
              <>
                <Divider />
                <CorrectVerificationDecisionForm
                  verificationId={data.id}
                  currentResult={data.result}
                  currentValidUntil={data.validUntil}
                  currentUnsuitableReason={data.unsuitableReason}
                />
              </>
            )}
          </SectionCard>
        )}
      </Box>
    </Stack>
  );
}
