import { useState } from "react";
import type { FormEvent } from "react";
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

function copyTextFallback(value: string): boolean {
  const textarea = document.createElement("textarea");
  textarea.value = value;
  textarea.setAttribute("readonly", "");
  textarea.style.position = "fixed";
  textarea.style.opacity = "0";
  document.body.appendChild(textarea);
  textarea.select();
  textarea.setSelectionRange(0, textarea.value.length);

  let copied = false;
  try {
    copied = document.execCommand("copy");
  } finally {
    textarea.remove();
  }

  return copied;
}

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
  const [copyStatus, setCopyStatus] = useState<"idle" | "success" | "error">("idle");

  const { data: users, isLoading, isError } = useUsers(includeArchived);
  const administration = useUserAdministration();
  const activeAdminCount =
    users?.filter(
      (user) => user.role === "admin" && user.isActive && !user.archived,
    ).length ?? 0;

  const handleCreate = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const normalizedUsername = username.trim();
    if (!normalizedUsername) return;

    administration.create.mutate(
      { username: normalizedUsername, role },
      {
        onSuccess: (user) => {
          setCreatedUser(user);
          setCopyStatus("idle");
          setUsername("");
        },
      },
    );
  };

  const mutationError =
    administration.create.isError ||
    administration.resetPassword.isError ||
    administration.changeRole.isError ||
    administration.changeStatus.isError ||
    administration.archive.isError ||
    administration.restore.isError;

  const handleCopyPassword = async () => {
    if (!createdUser) return;

    // Copy the exact value shown in the one-time password notice first.
    if (copyTextFallback(createdUser.temporaryPassword)) {
      setCopyStatus("success");
      return;
    }

    try {
      if (!navigator.clipboard?.writeText) {
        throw new Error("Clipboard API is unavailable");
      }
      await navigator.clipboard.writeText(createdUser.temporaryPassword);
      setCopyStatus("success");
    } catch {
      setCopyStatus("error");
    }
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
            slotProps={{ htmlInput: { maxLength: 100 } }}
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
              <Button color="inherit" onClick={() => { setCreatedUser(null); setCopyStatus("idle"); }}>
                Скрыть
              </Button>
            </Stack>
          }
        >
          <Typography sx={{ fontWeight: "bold" }}>
            Временный пароль для пользователя {createdUser.username}.
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
          {copyStatus === "success" && (
            <Typography role="status" color="success.dark">
              Пароль скопирован в буфер обмена.
            </Typography>
          )}
          {copyStatus === "error" && (
            <Typography role="alert" color="error">
              Не удалось скопировать пароль. Выделите его и скопируйте вручную.
            </Typography>
          )}
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
                    <FormControl size="small" fullWidth disabled={
                        user.archived ||
                        (user.role === "admin" && user.isActive && activeAdminCount <= 1) ||
                        administration.changeRole.isPending
                      }>
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
                    <Stack
                      direction="row"
                      spacing={1}
                      useFlexGap
                      sx={{ flexWrap: "wrap" }}
                    >
                      {!user.archived && user.isActive && (
                        <Button
                          size="small"
                          color="warning"
                          disabled={administration.resetPassword.isPending}
                          onClick={() => {
                            if (
                              window.confirm(
                                `Сбросить пароль пользователя ${user.username}? Все его активные сеансы будут завершены.`,
                              )
                            ) {
                              administration.resetPassword.mutate(user.id, {
                                onSuccess: (result) => {
                                  setCreatedUser(result);
                                  setCopyStatus("idle");
                                },
                              });
                            }
                          }}
                        >
                          Сбросить пароль
                        </Button>
                      )}
                      {!user.archived && (
                        <>
                          <Button
                            size="small"
                            disabled={
                              administration.changeStatus.isPending ||
                              (user.role === "admin" && user.isActive && activeAdminCount <= 1)
                            }
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
                            disabled={
                              administration.archive.isPending ||
                              (user.role === "admin" && user.isActive && activeAdminCount <= 1)
                            }
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
                      {user.role === "admin" &&
                        user.isActive &&
                        !user.archived &&
                        activeAdminCount <= 1 && (
                          <Typography variant="caption" color="text.secondary">
                            Последний активный администратор
                          </Typography>
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
