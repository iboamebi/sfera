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

import { useMaterials } from "../../features/materials/model/useMaterials";

type SortField = "name" | "article" | "unit" | "description" | "archived";
type SortDirection = "asc" | "desc";

export function MaterialsPage() {
  const { data: materials, isLoading, error } = useMaterials();
  const [search, setSearch] = useState("");
  const [sortField, setSortField] = useState<SortField>("name");
  const [sortDirection, setSortDirection] = useState<SortDirection>("asc");

  const filteredMaterials = useMemo(() => {
    const query = search.trim().toLocaleLowerCase("ru-RU");

    if (!query) {
      return materials ?? [];
    }

    return (materials ?? []).filter((material) =>
      [
        material.name,
        material.article,
        material.unit,
        material.description,
      ]
        .filter(Boolean)
        .some((value) => value!.toLocaleLowerCase("ru-RU").includes(query)),
    );
  }, [materials, search]);

  const sortedMaterials = useMemo(() => {
    return [...filteredMaterials].sort((left, right) => {
      const leftValue =
        sortField === "archived"
          ? left.archived ? "Да" : "Нет"
          : left[sortField] ?? "";
      const rightValue =
        sortField === "archived"
          ? right.archived ? "Да" : "Нет"
          : right[sortField] ?? "";

      return (
        leftValue.localeCompare(rightValue, "ru", { numeric: true }) *
        (sortDirection === "asc" ? 1 : -1)
      );
    });
  }, [filteredMaterials, sortDirection, sortField]);

  const handleSortClick = (field: SortField) => {
    if (sortField === field) {
      setSortDirection((current) => (current === "asc" ? "desc" : "asc"));
      return;
    }

    setSortField(field);
    setSortDirection("asc");
  };

  const columns: Array<{ field: SortField; label: string }> = [
    { field: "name", label: "Материал" },
    { field: "article", label: "Артикул" },
    { field: "unit", label: "Ед. измерения" },
    { field: "description", label: "Описание" },
    { field: "archived", label: "Статус" },
  ];

  if (isLoading) {
    return <Typography>Загрузка материалов...</Typography>;
  }

  if (error) {
    return <Typography>Не удалось загрузить материалы.</Typography>;
  }

  if (!materials || materials.length === 0) {
    return (
      <Stack spacing={2}>
        <Typography variant="h5">Материалы</Typography>
        <Typography color="text.secondary">Материалы пока не созданы.</Typography>
      </Stack>
    );
  }

  return (
    <Stack spacing={3}>
      <Typography variant="h5">Материалы</Typography>

      <TextField
        label="Поиск материалов"
        placeholder="Название, артикул, единица измерения или описание"
        value={search}
        onChange={(event) => setSearch(event.target.value)}
        size="small"
        fullWidth
      />

      {sortedMaterials.length === 0 && (
        <Typography color="text.secondary">
          По запросу «{search.trim()}» ничего не найдено.
        </Typography>
      )}

      {sortedMaterials.length > 0 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small" sx={{ minWidth: 800 }}>
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
              {sortedMaterials.map((material) => (
                <TableRow key={material.id} hover>
                  <TableCell>
                    <Link to={`/materials/${material.id}`}>
                      {material.name}
                    </Link>
                  </TableCell>
                  <TableCell>{material.article ?? "—"}</TableCell>
                  <TableCell>{material.unit}</TableCell>
                  <TableCell>{material.description ?? "—"}</TableCell>
                  <TableCell>
                    {material.archived ? "В архиве" : "Активен"}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Stack>
  );
}
