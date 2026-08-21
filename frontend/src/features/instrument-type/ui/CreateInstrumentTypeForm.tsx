import { useState } from "react";

import { Button, Stack, TextField, Typography } from "@mui/material";

interface CreateInstrumentTypeFormProps {
  isPending?: boolean;
  onSubmit: (data: { name: string }) => void;
  onCancel?: () => void;
}

export function CreateInstrumentTypeForm({
  isPending = false,
  onSubmit,
  onCancel,
}: CreateInstrumentTypeFormProps) {
  const [name, setName] = useState("");

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const trimmedName = name.trim();
    if (!trimmedName) {
      return;
    }

    onSubmit({ name: trimmedName });
  };

  return (
    <Stack component="form" spacing={2} onSubmit={handleSubmit}>
      <Typography variant="h6">Создание типа СИ</Typography>

      <TextField
        required
        label="Наименование типа СИ"
        value={name}
        onChange={(event) => setName(event.target.value)}
        disabled={isPending}
        autoFocus
      />

      <Stack direction="row" spacing={1}>
        <Button
          type="submit"
          variant="contained"
          disabled={!name.trim() || isPending}
        >
          {isPending ? "Создание…" : "Создать тип СИ"}
        </Button>

        {onCancel && (
          <Button type="button" onClick={onCancel} disabled={isPending}>
            Отмена
          </Button>
        )}
      </Stack>
    </Stack>
  );
}
