import { zodResolver } from "@hookform/resolvers/zod";
import {
  Autocomplete,
  Button,
  Divider,
  MenuItem,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { useQueryClient } from "@tanstack/react-query";

import { useCreateCustomer } from "../../../customers/model/useCreateCustomer";
import type { CreateCustomerSchema } from "../../../customers/model/schema";
import { CustomerForm } from "../../../customers/ui/CustomerForm";
import { useCustomers } from "../../../customers/model/useCustomers";
import type { DeviceRead } from "../../../devices/model/types";
import { useDevices } from "../../../devices/model/useDevices";
import { useOrders } from "../../model/useOrders";
import { createOrderSchema } from "../model/schema";
import type { CreateOrderForm as CreateOrderFormValues } from "../model/types";

interface CreateOrderFormProps {
  onSubmit: (data: CreateOrderFormValues) => void;
  isPending?: boolean;
}

function getLocalDateTimePlusDays(days: number): string {
  const date = new Date();
  date.setDate(date.getDate() + days);

  const pad = (value: number) => String(value).padStart(2, "0");

  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`;
}

function getNextOrderNumber(numbers: string[]): string {
  const numericNumbers = numbers
    .map((number) => Number(number))
    .filter((number) => Number.isInteger(number) && number >= 0);

  if (numericNumbers.length === 0) {
    return "1";
  }

  return String(Math.max(...numericNumbers) + 1);
}

export function CreateOrderForm({
  onSubmit,
  isPending = false,
}: CreateOrderFormProps) {
  const [isCreateCustomerOpen, setIsCreateCustomerOpen] = useState(false);
  const [createdCustomerId, setCreatedCustomerId] = useState<string>();
  const [selectedDevices, setSelectedDevices] = useState<DeviceRead[]>([]);
  const [selectedDevice, setSelectedDevice] = useState<DeviceRead | null>(null);
  const queryClient = useQueryClient();
  const {
    register,
    handleSubmit,
    setValue,
    getValues,
    formState: { errors, dirtyFields },
  } = useForm<CreateOrderFormValues>({
    resolver: zodResolver(createOrderSchema),
    defaultValues: {
      plannedIssueAt: getLocalDateTimePlusDays(14),
      instrumentIds: [],
    },
  });

  const {
    data: customers = [],
    isLoading: isCustomersLoading,
    isError: isCustomersError,
  } = useCustomers();
  const { data: orders = [], isLoading: isOrdersLoading } = useOrders();
  const { data: devices = [], isLoading: isDevicesLoading, isError: isDevicesError } =
    useDevices();

  useEffect(() => {
    if (isOrdersLoading || dirtyFields.number || getValues("number")) {
      return;
    }

    setValue("number", getNextOrderNumber(orders.map((order) => order.number)), {
      shouldValidate: true,
    });
  }, [dirtyFields.number, getValues, isOrdersLoading, orders, setValue]);

  useEffect(() => {
    if (!isCreateCustomerOpen && createdCustomerId) {
      setValue("customerId", createdCustomerId, { shouldValidate: true });
      setCreatedCustomerId(undefined);
    }
  }, [createdCustomerId, isCreateCustomerOpen, setValue]);

  const createCustomerMutation = useCreateCustomer({
    onSuccess: async (customer) => {
      await queryClient.invalidateQueries({ queryKey: ["customers"] });
      setCreatedCustomerId(customer.id);
      setIsCreateCustomerOpen(false);
    },
  });

  const handleCreateCustomer = (data: CreateCustomerSchema) => {
    createCustomerMutation.mutate(data);
  };

  const handleAddSelectedDevice = () => {
    if (!selectedDevice || selectedDevices.some((device) => device.id === selectedDevice.id)) {
      return;
    }

    const nextDevices = [...selectedDevices, selectedDevice];
    setSelectedDevices(nextDevices);
    setValue(
      "instrumentIds",
      nextDevices.map((device) => device.id),
      { shouldValidate: true },
    );
    setSelectedDevice(null);
  };

  const handleRemoveDevice = (deviceId: string) => {
    const nextDevices = selectedDevices.filter((device) => device.id !== deviceId);
    setSelectedDevices(nextDevices);
    setValue(
      "instrumentIds",
      nextDevices.map((device) => device.id),
      { shouldValidate: true },
    );
  };

  if (isCreateCustomerOpen) {
    return (
      <Stack spacing={2}>
        <CustomerForm
          onSubmit={handleCreateCustomer}
          isPending={createCustomerMutation.isPending}
        />
        <Button
          onClick={() => setIsCreateCustomerOpen(false)}
          disabled={createCustomerMutation.isPending}
        >
          Вернуться к заказу
        </Button>
      </Stack>
    );
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Stack spacing={2}>
        <TextField
          label="Номер заказа"
          {...register("number")}
          error={Boolean(errors.number)}
          helperText={errors.number?.message}
          disabled={isPending}
        />

        <TextField
          select
          label="Клиент"
          {...register("customerId")}
          error={Boolean(errors.customerId)}
          helperText={
            errors.customerId?.message ??
            (isCustomersError ? "Не удалось загрузить клиентов" : undefined)
          }
          disabled={isPending || isCustomersLoading || isCustomersError}
        >
          {customers
            .filter((customer) => !customer.archived)
            .map((customer) => (
              <MenuItem key={customer.id} value={customer.id}>
                {customer.name}
              </MenuItem>
            ))}
        </TextField>

        <Button
          onClick={() => setIsCreateCustomerOpen(true)}
          variant="outlined"
          disabled={isPending}
        >
          Создать клиента
        </Button>

        <TextField
          label="Планируемая дата выдачи"
          type="datetime-local"
          {...register("plannedIssueAt")}
          error={Boolean(errors.plannedIssueAt)}
          helperText={errors.plannedIssueAt?.message}
          disabled={isPending}
          slotProps={{
            inputLabel: {
              shrink: true,
            },
          }}
        />

        <Divider />

        <Stack spacing={2}>
          <Typography variant="h6">Позиции заказа</Typography>

          <Autocomplete
            options={devices.filter(
              (device) => !selectedDevices.some((selected) => selected.id === device.id),
            )}
            value={selectedDevice}
            loading={isDevicesLoading}
            disabled={isPending || isDevicesError}
            getOptionLabel={(device) => device.serialNumber}
            isOptionEqualToValue={(option, value) => option.id === value.id}
            onChange={(_, device) => setSelectedDevice(device)}
            renderInput={(params) => (
              <TextField
                {...params}
                label="Средство измерений"
                placeholder="Введите серийный номер"
                error={isDevicesError}
                helperText={
                  isDevicesError
                    ? "Не удалось загрузить средства измерений"
                    : undefined
                }
              />
            )}
          />

          <Button
            onClick={handleAddSelectedDevice}
            disabled={!selectedDevice || isPending}
            variant="outlined"
          >
            Добавить позицию
          </Button>

          {selectedDevices.length === 0 ? (
            <Typography color="text.secondary" variant="body2">
              Позиции отсутствуют
            </Typography>
          ) : (
            selectedDevices.map((device, index) => (
              <Stack
                key={device.id}
                direction="row"
                spacing={2}
                sx={{ alignItems: "center", justifyContent: "space-between" }}
              >
                <Typography variant="body2">
                  Позиция {index + 1}: СИ {device.serialNumber}
                </Typography>
                <Button
                  onClick={() => handleRemoveDevice(device.id)}
                  disabled={isPending}
                  size="small"
                >
                  Удалить
                </Button>
              </Stack>
            ))
          )}
        </Stack>

        <TextField
          label="Комментарий"
          multiline
          minRows={3}
          {...register("comment")}
          error={Boolean(errors.comment)}
          helperText={errors.comment?.message}
          disabled={isPending}
        />

        <Button
          type="submit"
          variant="contained"
          disabled={
            isPending ||
            isCustomersLoading ||
            isCustomersError ||
            isDevicesLoading ||
            isDevicesError
          }
        >
          {isPending ? "Создание..." : "Создать заказ"}
        </Button>
      </Stack>
    </form>
  );
}
