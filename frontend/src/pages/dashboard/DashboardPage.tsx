import type { ReactNode } from "react";

import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Divider,
  Stack,
  Typography,
} from "@mui/material";
import { Link } from "react-router";

import { useControlPanelOverview } from "../../features/control-panel/model/useControlPanelOverview";

const ORDER_STATUS_LABELS: Record<string, string> = {
  NEW: "Новые",
  REGISTERED: "Зарегистрированы",
  IN_WORK: "В работе",
  WAITING: "Ожидают",
  COMPLETED: "Завершены",
  ISSUED: "Выданы",
  CLOSED: "Закрыты",
  CANCELLED: "Отменены",
};

const VERIFICATION_STATUS_LABELS: Record<string, string> = {
  CREATED: "Созданы",
  IN_PROGRESS: "В работе",
  DECIDED: "Решение принято",
  CANCELLED: "Отменены",
};

const DEVICE_STATUS_LABELS: Record<string, string> = {
  AVAILABLE: "Доступны",
  IN_WORK: "В работе",
  WAITING: "Ожидают",
  COMPLETED: "Завершены",
  BLOCKED: "Заблокированы",
};

function MetricCard({
  title,
  value,
  description,
  href,
  children,
}: {
  title: string;
  value: string | number;
  description: string;
  href: string;
  children?: ReactNode;
}) {
  return (
    <Card variant="outlined">
      <CardContent>
        <Stack spacing={1.5}>
          <Typography color="text.secondary" variant="subtitle2">
            {title}
          </Typography>
          <Typography variant="h3">{value}</Typography>
          <Typography color="text.secondary" variant="body2">
            {description}
          </Typography>
          {children}
          <Button component={Link} to={href} size="small" sx={{ alignSelf: "flex-start" }}>
            Открыть раздел
          </Button>
        </Stack>
      </CardContent>
    </Card>
  );
}

export function DashboardPage() {
  const overviewQuery = useControlPanelOverview();

  if (overviewQuery.isPending) {
    return <Typography>Загрузка сводных данных...</Typography>;
  }

  if (overviewQuery.isError || !overviewQuery.data) {
    return (
      <Stack spacing={2}>
        <Typography variant="h4">Контрольная панель</Typography>
        <Alert severity="warning">
          Не удалось получить сводные данные. Проверьте доступность backend и повторите
          загрузку страницы.
        </Alert>
      </Stack>
    );
  }

  const overview = overviewQuery.data;

  return (
    <Stack spacing={3}>
      <Typography variant="h4">Контрольная панель</Typography>

      <Box>
        <Typography variant="h5" sx={{ mb: 2 }}>
          Состояние предприятия
        </Typography>
        <Box
          sx={{
            display: "grid",
            gridTemplateColumns: {
              xs: "1fr",
              sm: "repeat(2, minmax(0, 1fr))",
              xl: "repeat(4, minmax(0, 1fr))",
            },
            gap: 2,
          }}
        >
          <MetricCard
            title="Заказы"
            value={overview.orders.active_count}
            description={`Активные из ${overview.orders.total_count} неархивных заказов`}
            href="/orders"
          >
            <Divider />
            <Stack spacing={0.5}>
              {overview.orders.by_status.map(({ key, count }) => (
                <Stack key={key} direction="row" sx={{ justifyContent: "space-between" }}>
                  <Typography variant="body2">{ORDER_STATUS_LABELS[key] ?? key}</Typography>
                  <Typography variant="body2" sx={{ fontWeight: 600 }}>{count}</Typography>
                </Stack>
              ))}
            </Stack>
          </MetricCard>

          <MetricCard
            title="Поверки"
            value={overview.verifications.active_count}
            description={`Созданы или выполняются; всего ${overview.verifications.total_count} неархивных`}
            href="/verifications"
          >
            <Divider />
            <Stack spacing={0.5}>
              {overview.verifications.by_status.map(({ key, count }) => (
                <Stack key={key} direction="row" sx={{ justifyContent: "space-between" }}>
                  <Typography variant="body2">{VERIFICATION_STATUS_LABELS[key] ?? key}</Typography>
                  <Typography variant="body2" sx={{ fontWeight: 600 }}>{count}</Typography>
                </Stack>
              ))}
              {overview.verifications.by_result.map(({ key, count }) => (
                <Stack key={key} direction="row" sx={{ justifyContent: "space-between" }}>
                  <Typography variant="body2">
                    {key === "SUITABLE" ? "Пригодно" : key === "UNSUITABLE" ? "Непригодно" : key}
                  </Typography>
                  <Typography variant="body2" sx={{ fontWeight: 600 }}>{count}</Typography>
                </Stack>
              ))}
            </Stack>
          </MetricCard>

          <MetricCard
            title="Клиенты"
            value={overview.customers.active_count}
            description={`Действующие; в архиве: ${overview.customers.archived_count}`}
            href="/customers"
          />

          <MetricCard
            title="Средства измерений"
            value={overview.instruments.total_count}
            description="Всего учтено в справочнике СИ"
            href="/devices"
          >
            <Divider />
            <Stack spacing={0.5}>
              {overview.instruments.by_status.map(({ key, count }) => (
                <Stack key={key} direction="row" sx={{ justifyContent: "space-between" }}>
                  <Typography variant="body2">{DEVICE_STATUS_LABELS[key] ?? key}</Typography>
                  <Typography variant="body2" sx={{ fontWeight: 600 }}>{count}</Typography>
                </Stack>
              ))}
            </Stack>
          </MetricCard>
        </Box>
      </Box>

      <Box>
        <Typography variant="h5" sx={{ mb: 2 }}>
          Требует внимания
        </Typography>
        <Alert severity="info">
          Общий реестр отклонений, контроль сроков, задач и эскалаций пока не
          подключён. Этот блок не означает, что проблем нет: правила выявления
          ситуаций и информационные контракты модулей ещё предстоит реализовать.
        </Alert>
      </Box>
    </Stack>
  );
}
