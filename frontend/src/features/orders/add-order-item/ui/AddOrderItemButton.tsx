import { useState } from "react";

import { Button, Stack } from "@mui/material";

import { useCreateDevice } from "../../../devices/model/useCreateDevice";
import { CreateDeviceForm } from "../../../devices/ui/CreateDeviceForm";
import { useAddOrderItem } from "../model/useAddOrderItem";
import { DeviceSelector } from "./DeviceSelector";

interface AddOrderItemButtonProps {
  orderId: string;
}

export function AddOrderItemButton({ orderId }: AddOrderItemButtonProps) {
  const [deviceId, setDeviceId] = useState("");
  const [isCreateDeviceOpen, setIsCreateDeviceOpen] = useState(false);
  const addOrderItemMutation = useAddOrderItem(orderId);
  const createDeviceMutation = useCreateDevice();

  const handleAdd = () => {
    if (!deviceId) {
      return;
    }

    addOrderItemMutation.mutate(deviceId, {
      onSuccess: () => setDeviceId(""),
    });
  };

  const handleCreateDevice = (data: {
    instrumentTypeId: string;
    serialNumber: string;
  }) => {
    createDeviceMutation.mutate(data, {
      onSuccess: (device) => {
        setDeviceId(device.id);
        setIsCreateDeviceOpen(false);
      },
    });
  };

  if (isCreateDeviceOpen) {
    return (
      <CreateDeviceForm
        isPending={createDeviceMutation.isPending}
        onSubmit={handleCreateDevice}
      />
    );
  }

  return (
    <Stack direction="row" spacing={2} sx={{ alignItems: "center" }}>
      <DeviceSelector
        value={deviceId}
        onChange={setDeviceId}
        onCreateDevice={() => setIsCreateDeviceOpen(true)}
      />

      <Button
        disabled={!deviceId || addOrderItemMutation.isPending}
        onClick={handleAdd}
        variant="outlined"
      >
        {addOrderItemMutation.isPending ? "Добавление…" : "Добавить позицию"}
      </Button>
    </Stack>
  );
}
