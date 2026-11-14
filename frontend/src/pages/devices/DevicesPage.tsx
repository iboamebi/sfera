import { useMemo, useState } from "react";
import {
  Button,
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";
import { Link } from "react-router";

import type { DeviceRead } from "../../features/devices/model/types";
import { useDevices } from "../../features/devices/model/useDevices";

type SortField = "name" | "serialNumber" | "registryNumber" | "modification" | "status";
type SortDirection = "asc" | "desc";

export function DevicesPage() {
  const { data: devices, isLoading, error } = useDevices();
  const [search, setSearch] = useState("");
  const [sortField, setSortField] = useState<SortField>("name");
  const [sortDirection, setSortDirection] = useState<SortDirection>("asc");

  const filteredDevices = useMemo(() => {
    const query = search.trim().toLocaleLowerCase("ru-RU");

    if (!query) {
      return devices ?? [];
    }

    return (devices ?? []).filter((device) =>
      [
        device.name,
        device.serialNumber,
        device.registryNumber,
        device.modification,
        device.inventoryNumber,
        device.status,
      ]
        .filter(Boolean)
        .some((value) => value!.toLocaleLowerCase("ru-RU").includes(query)),
    );
  }, [devices, search]);

  const sortedDevices = useMemo(() => {
    return [...filteredDevices].sort((left, right) => {
      const leftValue = left[sortField] ?? "";
      const rightValue = right[sortField] ?? "";

      return (
        leftValue.localeCompare(rightValue, "ru", { numeric: true }) *
        (sortDirection === "asc" ? 1 : -1)
      );
    });
  }, [filteredDevices, sortDirection, sortField]);

  const handleSortClick = (field: SortField) => {
    if (sortField === field) {
      setSortDirection((current) => (current === "asc" ? "desc" : "asc"));
      return;
    }

    setSortField(field);
    setSortDirection("asc");
  };

  const columns: Array<{ field: SortField; label: string }> = [
    { field: "name", label: "СИ" },
    { field: "serialNumber", label: "Серийный номер" },
    { field: "registryNumber", label: "Регистрационный номер" },
    { field: "modification", label: "Модификация" },
    { field: "status", label: "Статус" },
  ];

  if (isLoading) {
    return <Typography>Загрузка средств измерений...</Typography>;
  }

  if (error) {
    return <Typography>Не удалось загрузить средства измерений.</Typography>;
  }

  return (
    <Stack spacing={2}>
      <Stack
        direction="row"
        spacing={2}
        sx={{
          alignItems: { xs: "stretch", sm: "center" },
          justifyContent: "space-between",
          flexWrap: "wrap",
        }}
      >
        <Typography variant="h5">Средства измерений</Typography>
        <Button component={Link} to="/devices/new" variant="contained">
          Создать СИ
        </Button>
      </Stack>

      <TextField
        label="Поиск СИ"
        placeholder="Наименование, серийный или регистрационный номер"
        value={search}
        onChange={(event) => setSearch(event.target.value)}
        size="small"
        fullWidth
      />

      {devices && devices.length === 0 && (
        <Typography color="text.secondary">
          Средства измерений отсутствуют.
        </Typography>
      )}

      {devices && devices.length > 0 && sortedDevices.length === 0 && (
        <Typography color="text.secondary">
          По запросу «{search.trim()}» ничего не найдено.
        </Typography>
      )}

      {sortedDevices.length > 0 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small" sx={{ minWidth: 900 }}>
            <TableHead>
              <TableRow>
                {columns.map(({ field, label }) => (
                  <TableCell
                    key={field}
                    sx={{ fontWeight: 700, whiteSpace: "nowrap" }}
                  >
                    <Button
                      size="small"
                      color="inherit"
                      onClick={() => handleSortClick(field)}
                      sx={{
                        minWidth: 0,
                        px: 0.5,
                        fontWeight: 700,
                        textTransform: "none",
                      }}
                    >
                      {label}{" "}
                      {sortField === field &&
                        (sortDirection === "asc" ? "↑" : "↓")}
                    </Button>
                  </TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {sortedDevices.map((device: DeviceRead) => (
                <TableRow key={device.id} hover>
                  <TableCell>
                    <Link to={`/devices/${device.id}`}>
                      {device.name ?? "Без наименования"}
                    </Link>
                  </TableCell>
                  <TableCell>{device.serialNumber}</TableCell>
                  <TableCell>{device.registryNumber ?? "—"}</TableCell>
                  <TableCell>{device.modification ?? "—"}</TableCell>
                  <TableCell>{device.status}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Stack>
  );
}
