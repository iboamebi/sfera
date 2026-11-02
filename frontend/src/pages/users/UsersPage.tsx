import { useState } from "react";
import {
  Alert,
  Button,
  Checkbox,
  FormControl,
  FormControlLabel,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";

import type { UserCreated, UserRead, UserRole } from "../../features/users/model/types";
import { useUserAdministration } from "../../features/users/model/useUserAdministration";
import { useUsers } from "../../features/users/model/useUsers";

const roles: UserRole[] = [
  "admin",
  "operator",
  "metrologist",
  "technician",
  "warehouse",
];

const roleLabels: Record<UserRole, string> = {
  admin: "Администратор",
  operator: "Оператор",
  metrologist: "Метролог",
  technician: "Техник",
  warehouse: "Склад",
};

function userStatus(user: UserRead): string {
  if (user.archived) return "В архиве";
  if (!user.isActive) return "Неактивен";
  if (user.mustChangePassword) return "Ожидает смены пароля";
  return "Активен";
}

export function UsersPage() {
  const [includeArchived, setIncludeArchived] = useState(false);
  const [username, setUsername] = useState("");
  const [role, setRole] = useState<UserRole>("operator");
  const [createdUser, setCreatedUser] = useState<UserCreated | null>(null);

  const { data: users, isLoading, isError } = useUsers(includeArchived);
  const administration = useUserAdministration();

  const handleCreate = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const normalizedUsername = username.trim();
    if (!normalizedUsername) return;

    administration.create.mutate(
      { username: normalizedUsername, role },
      {
        onSuccess: (user) => {
          setCreatedUser(user);
          setUsername("");
        },
      },
    );
  };

  const mutationError =
    administration.create.isError ||
    administration.changeRole.isError ||
    administration.changeStatus.isError ||
    administration.archive.isError ||
    administration.restore.isError;

  const handleCopyPassword = async () => {
    if (!createdUser) return;
    await navigator.clipboard.writeText(createdUser.temporaryPassword);
  };

  return (
    <Stack spacing={3}>
      <Typography variant="h4">Пользователи</Typography>

      <Paper component="form" onSubmit={handleCreate} sx={{ p: 2 }}>
        <Stack spacing={2}>
          <Typography variant="h6">Создать пользователя</Typography>
          <TextField
            label="Имя пользователя"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            inputProps={{ maxLength: 100 }}
            required
            fullWidth
          />
          <FormControl fullWidth>
            <InputLabel id="new-user-role-label">Роль</InputLabel>
            <Select
              labelId="new-user-role-label"
              label="Роль"
              value={role}
              onChange={(event) => setRole(event.target.value as UserRole)}
            >
              {roles.map((item) => (
                <MenuItem key={item} value={item}>
                  {roleLabels[item]}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <Button
            type="submit"
            variant="contained"
            disabled={administration.create.isPending}
          >
            {administration.create.isPending ? "Создание..." : "Создать пользователя"}
          </Button>
        </Stack>
      </Paper>

      {createdUser && (
        <Alert
          severity="success"
          action={
            <Stack direction="row" spacing={1}>
              <Button color="inherit" onClick={handleCopyPassword}>
                Копировать пароль
              </Button>
              <Button color="inherit" onClick={() => setCreatedUser(null)}>
                Скрыть
              </Button>
            </Stack>
          }
        >
          <Typography fontWeight="bold">
            Пользователь {createdUser.username} создан.
          </Typography>
          <Typography>
            Временный пароль (показывается только в этом сообщении):
          </Typography>
          <Typography component="code" sx={{ overflowWrap: "anywhere" }}>
            {createdUser.temporaryPassword}
          </Typography>
          <Typography>
            При первом входе пользователь должен сменить пароль.
          </Typography>
        </Alert>
      )}

      {mutationError && (
        <Alert severity="error">
          Операция не выполнена. Проверьте данные и права доступа, затем повторите.
        </Alert>
      )}

      <Stack spacing={1}>
        <Typography variant="h6">Список пользователей</Typography>
        <FormControlLabel
          control={
            <Checkbox
              checked={includeArchived}
              onChange={(event) => setIncludeArchived(event.target.checked)}
            />
          }
          label="Показывать архивные аккаунты"
        />
      </Stack>

      {isLoading && <Typography>Загрузка пользователей...</Typography>}
      {isError && (
        <Alert severity="error">
          Не удалось загрузить пользователей. Убедитесь, что у вашей учётной записи есть права администратора.
        </Alert>
      )}
      {!isLoading && !isError && users?.length === 0 && (
        <Typography>Пользователи не найдены.</Typography>
      )}

      {users && users.length > 0 && (
        <Paper sx={{ overflowX: "auto" }}>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Имя пользователя</TableCell>
                <TableCell>Роль</TableCell>
                <TableCell>Статус</TableCell>
                <TableCell>Действия</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {users.map((user) => (
                <TableRow key={user.id}>
                  <TableCell>{user.username}</TableCell>
                  <TableCell sx={{ minWidth: 190 }}>
                    <FormControl size="small" fullWidth disabled={user.archived || administration.changeRole.isPending}>
                      <Select
                        aria-label={`Роль пользователя ${user.username}`}
                        value={user.role}
                        onChange={(event) =>
                          administration.changeRole.mutate({
                            userId: user.id,
                            role: event.target.value as UserRole,
                          })
                        }
                      >
                        {roles.map((item) => (
                          <MenuItem key={item} value={item}>
                            {roleLabels[item]}
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                  </TableCell>
                  <TableCell>{userStatus(user)}</TableCell>
                  <TableCell>
                    <Stack direction="row" spacing={1} useFlexGap flexWrap="wrap">
                      {!user.archived && (
                        <>
                          <Button
                            size="small"
                            disabled={administration.changeStatus.isPending}
                            onClick={() =>
                              administration.changeStatus.mutate({
                                userId: user.id,
                                isActive: !user.isActive,
                              })
                            }
                          >
                            {user.isActive ? "Деактивировать" : "Активировать"}
                          </Button>
                          <Button
                            size="small"
                            color="warning"
                            disabled={administration.archive.isPending}
                            onClick={() => {
                              if (window.confirm(`Архивировать пользователя ${user.username}?`)) {
                                administration.archive.mutate(user.id);
                              }
                            }}
                          >
                            Архивировать
                          </Button>
                        </>
                      )}
                      {user.archived && (
                        <Button
                          size="small"
                          disabled={administration.restore.isPending}
                          onClick={() => administration.restore.mutate(user.id)}
                        >
                          Восстановить
                        </Button>
                      )}
                    </Stack>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
      )}
    </Stack>
  );
}
