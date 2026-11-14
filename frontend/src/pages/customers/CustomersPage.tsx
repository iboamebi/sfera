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

import { useCustomers } from "../../features/customers/model/useCustomers";

type SortField = "name" | "contactPerson" | "phone" | "email" | "archived";
type SortDirection = "asc" | "desc";

export function CustomersPage() {
  const { data: customers, isLoading, error } = useCustomers();
  const [search, setSearch] = useState("");
  const [sortField, setSortField] = useState<SortField>("name");
  const [sortDirection, setSortDirection] = useState<SortDirection>("asc");

  const filteredCustomers = useMemo(() => {
    const query = search.trim().toLocaleLowerCase("ru-RU");

    if (!query) {
      return customers ?? [];
    }

    return (customers ?? []).filter((customer) =>
      [
        customer.name,
        customer.contactPerson,
        customer.phone,
        customer.email,
      ]
        .filter(Boolean)
        .some((value) => value!.toLocaleLowerCase("ru-RU").includes(query)),
    );
  }, [customers, search]);

  const sortedCustomers = useMemo(() => {
    return [...filteredCustomers].sort((left, right) => {
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
  }, [filteredCustomers, sortDirection, sortField]);

  const handleSortClick = (field: SortField) => {
    if (sortField === field) {
      setSortDirection((current) => (current === "asc" ? "desc" : "asc"));
      return;
    }

    setSortField(field);
    setSortDirection("asc");
  };

  const columns: Array<{ field: SortField; label: string }> = [
    { field: "name", label: "Клиент" },
    { field: "contactPerson", label: "Контактное лицо" },
    { field: "phone", label: "Телефон" },
    { field: "email", label: "E-mail" },
    { field: "archived", label: "Статус" },
  ];

  if (isLoading) {
    return <Typography>Загрузка клиентов...</Typography>;
  }

  if (error) {
    return <Typography>Не удалось загрузить клиентов.</Typography>;
  }

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
        <Typography variant="h4">Клиенты</Typography>
        <Button component={Link} to="/customers/new" variant="contained">
          Создать клиента
        </Button>
      </Stack>

      <TextField
        label="Поиск клиентов"
        placeholder="Название, контактное лицо, телефон или e-mail"
        value={search}
        onChange={(event) => setSearch(event.target.value)}
        size="small"
        fullWidth
      />

      {customers && customers.length === 0 && (
        <Typography color="text.secondary">Клиенты пока не созданы.</Typography>
      )}

      {customers && customers.length > 0 && sortedCustomers.length === 0 && (
        <Typography color="text.secondary">
          По запросу «{search.trim()}» ничего не найдено.
        </Typography>
      )}

      {sortedCustomers.length > 0 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small" sx={{ minWidth: 760 }}>
            <TableHead>
              <TableRow>
                {columns.map(({ field, label }) => (
                  <TableCell key={field} sx={{ fontWeight: 700, whiteSpace: "nowrap" }}>
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
              {sortedCustomers.map((customer) => (
                <TableRow key={customer.id} hover>
                  <TableCell>
                    <Link to={`/customers/${customer.id}`}>
                      {customer.name}
                    </Link>
                  </TableCell>
                  <TableCell>{customer.contactPerson ?? "—"}</TableCell>
                  <TableCell>{customer.phone ?? "—"}</TableCell>
                  <TableCell>{customer.email ?? "—"}</TableCell>
                  <TableCell>
                    {customer.archived ? "В архиве" : "Активен"}
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
