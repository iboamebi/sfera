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

import { useCustomers } from "../../features/customers/model/useCustomers";
import { useDevices } from "../../features/devices/model/useDevices";
import { useOrders } from "../../features/orders/model/useOrders";
import { useVerifications } from "../../features/verifications/model/useVerifications";

const ORDER_ACTIVE_STATUSES = new Set([
  "NEW",
  "REGISTERED",
  "IN_WORK",
  "WAITING",
]);

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

const VERIFICATION_STATUS_LABELS = {
  CREATED: "Созданы",
  IN_PROGRESS: "В работе",
  DECIDED: "Решение принято",
  CANCELLED: "Отменены",
} as const;

const DEVICE_STATUS_LABELS = {
  AVAILABLE: "Доступны",
  IN_WORK: "В работе",
  WAITING: "Ожидают",
  COMPLETED: "Завершены",
  BLOCKED: "Заблокированы",
} as const;

function countBy<T extends string>(
  values: T[],
): Array<{ status: T; count: number }> {
  const counts = new Map<T, number>();

  for (const value of values) {
    counts.set(value, (counts.get(value) ?? 0) + 1);
  }

  return Array.from(counts, ([status, count]) => ({ status, count }));
}

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
  const ordersQuery = useOrders();
  const verificationsQuery = useVerifications();
  const customersQuery = useCustomers();
  const devicesQuery = useDevices();

  const orders = (ordersQuery.data ?? []).filter((order) => !order.archived);
  const verifications = (verificationsQuery.data ?? []).filter(
    (verification) => !verification.archived,
  );
  const customers = customersQuery.data ?? [];
  const devices = devicesQuery.data ?? [];

  const orderCounts = countBy(orders.map((order) => order.status));
  const verificationCounts = countBy(
    verifications.map((verification) => verification.status),
  );
  const deviceCounts = countBy(devices.map((device) => device.status));

  const activeOrders = orders.filter((order) =>
    ORDER_ACTIVE_STATUSES.has(order.status),
  ).length;
  const activeVerifications = verifications.filter(
    (verification) =>
      verification.status === "CREATED" ||
      verification.status === "IN_PROGRESS",
  ).length;
  const activeCustomers = customers.filter((customer) => !customer.archived).length;
  const archivedCustomers = customers.length - activeCustomers;

  const queries = [
    ordersQuery,
    verificationsQuery,
    customersQuery,
    devicesQuery,
  ];
  const hasError = queries.some((query) => query.isError);
  const isLoading = queries.some((query) => query.isPending);

  if (isLoading) {
    return <Typography>Загрузка сводных данных...</Typography>;
  }

  return (
    <Stack spacing={3}>
      <Typography variant="h4">Контрольная панель</Typography>

      {hasError && (
        <Alert severity="warning">
          Не все источники данных доступны. Показатели ниже могут быть неполными.
          Проверьте соответствующие рабочие разделы.
        </Alert>
      )}

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
          {!ordersQuery.isError && (
            <MetricCard
              title="Заказы"
              value={activeOrders}
              description={`Активные из ${orders.length} неархивных заказов`}
              href="/orders"
            >
              <Divider />
              <Stack spacing={0.5}>
                {orderCounts.map(({ status, count }) => (
                  <Stack key={status} direction="row" justifyContent="space-between">
                    <Typography variant="body2">
                      {ORDER_STATUS_LABELS[status] ?? status}
                    </Typography>
                    <Typography variant="body2" fontWeight={600}>
                      {count}
                    </Typography>
                  </Stack>
                ))}
              </Stack>
            </MetricCard>
          )}

          {!verificationsQuery.isError && (
            <MetricCard
              title="Поверки"
              value={activeVerifications}
              description={`Созданы или выполняются; всего ${verifications.length} неархивных`}
              href="/verifications"
            >
              <Divider />
              <Stack spacing={0.5}>
                {verificationCounts.map(({ status, count }) => (
                  <Stack key={status} direction="row" justifyContent="space-between">
                    <Typography variant="body2">
                      {VERIFICATION_STATUS_LABELS[status]}
                    </Typography>
                    <Typography variant="body2" fontWeight={600}>
                      {count}
                    </Typography>
                  </Stack>
                ))}
                <Stack direction="row" justifyContent="space-between">
                  <Typography variant="body2">Пригодно</Typography>
                  <Typography variant="body2" fontWeight={600}>
                    {verifications.filter((item) => item.result === "SUITABLE").length}
                  </Typography>
                </Stack>
                <Stack direction="row" justifyContent="space-between">
                  <Typography variant="body2">Непригодно</Typography>
                  <Typography variant="body2" fontWeight={600}>
                    {verifications.filter((item) => item.result === "UNSUITABLE").length}
                  </Typography>
                </Stack>
              </Stack>
            </MetricCard>
          )}

          {!customersQuery.isError && (
            <MetricCard
              title="Клиенты"
              value={activeCustomers}
              description={`Действующие; в архиве: ${archivedCustomers}`}
              href="/customers"
            />
          )}

          {!devicesQuery.isError && (
            <MetricCard
              title="Средства измерений"
              value={devices.length}
              description="Всего учтено в справочнике СИ"
              href="/devices"
            >
              <Divider />
              <Stack spacing={0.5}>
                {deviceCounts.map(({ status, count }) => (
                  <Stack key={status} direction="row" justifyContent="space-between">
                    <Typography variant="body2">
                      {DEVICE_STATUS_LABELS[status] ?? status}
                    </Typography>
                    <Typography variant="body2" fontWeight={600}>
                      {count}
                    </Typography>
                  </Stack>
                ))}
              </Stack>
            </MetricCard>
          )}
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
