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
import { useSites } from "../../features/sites/model/useSites";

export function SitesPage() {
  const { data: sites, isLoading, error } = useSites();
  const { data: customers } = useCustomers();
  const [search, setSearch] = useState("");

  const customerNames = useMemo(
    () => new Map((customers ?? []).map((customer) => [customer.id, customer.name])),
    [customers],
  );

  const filteredSites = useMemo(() => {
    const query = search.trim().toLocaleLowerCase("ru-RU");

    if (!query) {
      return sites ?? [];
    }

    return (sites ?? []).filter((site) =>
      [site.name, site.address, customerNames.get(site.customerId) ?? ""]
        .some((value) => value.toLocaleLowerCase("ru-RU").includes(query)),
    );
  }, [customerNames, search, sites]);

  const sortedSites = useMemo(
    () => [...filteredSites].sort((left, right) =>
      left.name.localeCompare(right.name, "ru", { numeric: true }),
    ),
    [filteredSites],
  );

  if (isLoading) {
    return <Typography>Загрузка узлов...</Typography>;
  }

  if (error) {
    return <Typography color="error">Не удалось загрузить узлы.</Typography>;
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
        <Typography variant="h4">Узлы</Typography>
        <Button component={Link} to="/sites/new" variant="contained">
          Создать узел
        </Button>
      </Stack>

      <TextField
        label="Поиск узлов"
        placeholder="Название, адрес или клиент"
        value={search}
        onChange={(event) => setSearch(event.target.value)}
        size="small"
        fullWidth
      />

      {sites && sites.length === 0 && (
        <Typography color="text.secondary">Узлы пока не созданы.</Typography>
      )}

      {sites && sites.length > 0 && sortedSites.length === 0 && (
        <Typography color="text.secondary">
          По запросу «{search.trim()}» ничего не найдено.
        </Typography>
      )}

      {sortedSites.length > 0 && (
        <TableContainer component={Paper} variant="outlined">
          <Table size="small" sx={{ minWidth: 640 }}>
            <TableHead>
              <TableRow>
                <TableCell sx={{ fontWeight: 700 }}>Узел</TableCell>
                <TableCell sx={{ fontWeight: 700 }}>Адрес</TableCell>
                <TableCell sx={{ fontWeight: 700 }}>Клиент</TableCell>
                <TableCell sx={{ fontWeight: 700 }}>Статус</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {sortedSites.map((site) => (
                <TableRow key={site.id} hover>
                  <TableCell>
                    <Link to={`/sites/${site.id}`}>{site.name}</Link>
                  </TableCell>
                  <TableCell>{site.address}</TableCell>
                  <TableCell>
                    <Link to={`/customers/${site.customerId}`}>
                      {customerNames.get(site.customerId) ?? "Клиент не найден"}
                    </Link>
                  </TableCell>
                  <TableCell>{site.archived ? "В архиве" : "Активен"}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Stack>
  );
}
