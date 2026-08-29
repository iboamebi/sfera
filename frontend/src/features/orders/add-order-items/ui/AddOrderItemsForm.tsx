import { useState } from "react";

import {
  Alert,
  Button,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Stack,
  TextField,
} from "@mui/material";

import type { OrderItemOperation } from "../../model/types";
import { useInstrumentTypes } from "../../../instrument-type/model/useInstrumentTypes";
import { useAddOrderItems } from "../model/useAddOrderItems";

const DEFAULT_OPERATIONS: OrderItemOperation[] = ["verification"];

interface AddOrderItemsFormProps {
  orderId: string;
}

export function AddOrderItemsForm({ orderId }: AddOrderItemsFormProps) {
  const [instrumentTypeId, setInstrumentTypeId] = useState("");
  const [quantity, setQuantity] = useState(1);
  const mutation = useAddOrderItems(orderId);
  const { data: instrumentTypes = [], isLoading, error } = useInstrumentTypes();

  const handleSubmit = () => {
    if (!instrumentTypeId || quantity < 1) {
      return;
    }

    mutation.mutate(
      {
        instrumentTypeId,
        quantity,
        requestedOperations: DEFAULT_OPERATIONS,
      },
      {
        onSuccess: () => {
          setQuantity(1);
        },
      },
    );
  };

  return (
    <Stack spacing={1} sx={{ minWidth: 320 }}>
      <FormControl fullWidth disabled={isLoading || mutation.isPending}>
        <InputLabel id="mass-intake-instrument-type-label">
          Тип СИ
        </InputLabel>
        <Select
          labelId="mass-intake-instrument-type-label"
          value={instrumentTypeId}
          label="Тип СИ"
          onChange={(event) => {
            setInstrumentTypeId(event.target.value);
            mutation.reset();
          }}
        >
          {instrumentTypes
            .filter((instrumentType) => !instrumentType.archived)
            .map((instrumentType) => (
              <MenuItem key={instrumentType.id} value={instrumentType.id}>
                {instrumentType.name}
                {instrumentType.model ? ` — ${instrumentType.model}` : ""}
              </MenuItem>
            ))}
        </Select>
      </FormControl>

      <TextField
        fullWidth
        label="Количество"
        type="number"
        inputProps={{ min: 1, step: 1 }}
        value={quantity}
        disabled={mutation.isPending}
        onChange={(event) => setQuantity(Number(event.target.value))}
      />

      <Button
        variant="contained"
        disabled={!instrumentTypeId || quantity < 1 || mutation.isPending}
        onClick={handleSubmit}
      >
        {mutation.isPending ? "Приёмка…" : "Принять количество"}
      </Button>

      {error && (
        <Alert severity="error">Не удалось выполнить массовую приёмку.</Alert>
      )}

      {mutation.isSuccess && (
        <Alert severity="success">
          Добавлено позиций: {quantity}. Карточки СИ можно заполнить позже.
        </Alert>
      )}
    </Stack>
  );
}
