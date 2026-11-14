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

import { useOrganizations } from "../../features/organizations/model/useOrganizations";

type SortField = "name" | "shortName" | "inn" | "address" | "phone" | "email";
type SortDirection = "asc" | "desc";

export function OrganizationsPage() {
  const { data: organizations, isLoading, error } = useOrganizations();
  const [search, setSearch] = useState("");
  const [sortField, setSortField] = useState<SortField>("name");
  const [sortDirection, setSortDirection] = useState<SortDirection>("asc");

  const filteredOrganizations = useMemo(() => {
    const query = search.trim().toLocaleLowerCase("ru-RU");

    if (!query) {
      return organizations ?? [];
    }

    return (organizations ?? []).filter((organization) =>
      [
        organization.name,
        organization.shortName,
        organization.inn,
        organization.address,
        organization.phone,
        organization.email,
      ]
        .filter(Boolean)
        .some((value) => value!.toLocaleLowerCase("ru-RU").includes(query)),
    );
  }, [organizations, search]);

  const sortedOrganizations = useMemo(() => {
    return [...filteredOrganizations].sort((left, right) => {
      const leftValue = left[sortField] ?? "";
      const rightValue = right[sortField] ?? "";

      return (
        leftValue.localeCompare(rightValue, "ru", { numeric: true }) *
        (sortDirection === "asc" ? 1 : -1)
      );
    });
  }, [filteredOrganizations, sortDirection, sortField]);

  const handleSortClick = (field: SortField) => {
    if (sortField === field) {
      setSortDirection((current) => (current === "asc" ? "desc" : "asc"));
      return;
    }

    setSortField(field);
    setSortDirection("asc");
  };

  const columns: Array<{ field: SortField; label: string }> = [
    { field: "name", label: "Организация" },
    { field: "shortName", label: "Краткое наименование" },
    { field: "inn", label: "ИНН" },
    { field: "address", label: "Адрес" },
    { field: "phone", label: "Телефон" },
    { field: "email", label: "E-mail" },
  ];

  return (
    <Stack spacing={3}>
      <Stack
        direction="row"
        spacing={2}
        sx={{
          alignItems: { xs: "stretch", sm: "center" },
          justifyContent: "space-between",
          flexWrap: "wrap",
        }}
      >
        <Typography variant="h4">Организации</Typography>
        <Button component={Link} to="/organizations/new" variant="contained">
          Создать организацию
        </Button>
      </Stack>

      {isLoading && <Typography>Загрузка организаций...</Typography>}

      {error && (
        <Typography color="error">
          Не удалось загрузить организации.
        </Typography>
      )}

      {!isLoading && !error && (
        <>
          <TextField
            label="Поиск организаций"
            placeholder="Название, ИНН, адрес, телефон или e-mail"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            size="small"
            fullWidth
          />

          {(!organizations || organizations.length === 0) && (
            <Typography color="text.secondary">
              Организации пока не созданы.
            </Typography>
          )}

          {organizations && organizations.length > 0 && sortedOrganizations.length === 0 && (
            <Typography color="text.secondary">
              По запросу «{search.trim()}» ничего не найдено.
            </Typography>
          )}

          {sortedOrganizations.length > 0 && (
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
                  {sortedOrganizations.map((organization) => (
                    <TableRow key={organization.id} hover>
                      <TableCell>
                        <Link to={`/organizations/${organization.id}`}>
                          {organization.name}
                        </Link>
                      </TableCell>
                      <TableCell>{organization.shortName ?? "—"}</TableCell>
                      <TableCell>{organization.inn ?? "—"}</TableCell>
                      <TableCell>{organization.address ?? "—"}</TableCell>
                      <TableCell>{organization.phone ?? "—"}</TableCell>
                      <TableCell>{organization.email ?? "—"}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </>
      )}
    </Stack>
  );
}
