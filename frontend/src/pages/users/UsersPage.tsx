import { useMemo, useState } from "react";
import type { FormEvent } from "react";
import {
  Alert,
  Button,
  Checkbox,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
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

import type {
  UserCreateInput,
  UserCreated,
  UserRead,
  UserRole,
} from "../../features/users/model/types";
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

function employeeName(user: UserRead): string {
  return user.fullName?.trim() || "ФИО не указано";
}

function matchesSearch(user: UserRead, query: string): boolean {
  const normalized = query.trim().toLocaleLowerCase("ru-RU");
  if (!normalized) return true;

  return [
    user.fullName,
    user.username,
    user.phone,
    user.position,
    roleLabels[user.role],
  ].some((value) => value?.toLocaleLowerCase("ru-RU").includes(normalized));
}

export function UsersPage() {
  const [includeArchived, setIncludeArchived] = useState(false);
  const [search, setSearch] = useState("");
  const [fullName, setFullName] = useState("");
  const [username, setUsername] = useState("");
  const [phone, setPhone] = useState("");
  const [position, setPosition] = useState("");
  const [role, setRole] = useState<UserRole>("operator");
  const [createdUser, setCreatedUser] = useState<UserCreated | null>(null);
  const [copyStatus, setCopyStatus] = useState<"idle" | "success" | "error">("idle");
  const [editingUser, setEditingUser] = useState<UserRead | null>(null);
  const [editFullName, setEditFullName] = useState("");
  const [editPhone, setEditPhone] = useState("");
  const [editPosition, setEditPosition] = useState("");

  const { data: users, isLoading, isError } = useUsers(includeArchived);
  const administration = useUserAdministration();

  const activeAdminCount =
    users?.filter(
      (user) => user.role === "admin" && user.isActive && !user.archived,
    ).length ?? 0;

  const visibleUsers = useMemo(
    () => users?.filter((user) => matchesSearch(user, search)) ?? [],
    [users, search],
  );

  const handleCreate = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data: UserCreateInput = {
      fullName: fullName.trim(),
      username: username.trim(),
      phone,
      position,
      role,
    };
    if (!data.fullName || !data.username) return;

    administration.create.mutate(data, {
      onSuccess: (user) => {
        setCreatedUser(user);
        setCopyStatus("idle");
        setFullName("");
        setUsername("");
        setPhone("");
        setPosition("");
      },
    });
  };

  const openProfile = (user: UserRead) => {
    setEditingUser(user);
    setEditFullName(user.fullName ?? "");
    setEditPhone(user.phone ?? "");
    setEditPosition(user.position ?? "");
  };

  const handleProfileSave = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!editingUser || !editFullName.trim()) return;

    administration.updateProfile.mutate(
      {
        userId: editingUser.id,
        data: {
          fullName: editFullName.trim(),
          phone: editPhone,
          position: editPosition,
        },
      },
      {
        onSuccess: () => setEditingUser(null),
      },
    );
  };

  const mutationError =
    administration.create.isError ||
    administration.updateProfile.isError ||
    administration.resetPassword.isError ||
    administration.changeRole.isError ||
    administration.changeStatus.isError ||
    administration.archive.isError ||
    administration.restore.isError;

  const handleCopyPassword = async () => {
    if (!createdUser) return;

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
      <Typography variant="h4">Сотрудники и пользователи</Typography>

      <Paper component="form" onSubmit={handleCreate} sx={{ p: 2 }}>
        <Stack spacing={2}>
          <Typography variant="h6">Создать учётную запись сотрудника</Typography>
          <Stack direction={{ xs: "column", md: "row" }} spacing={2}>
            <TextField
              label="ФИО"
              value={fullName}
              onChange={(event) => setFullName(event.target.value)}
              slotProps={{ htmlInput: { maxLength: 255 } }}
              required
              fullWidth
            />
            <TextField
              label="Логин для входа"
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              slotProps={{ htmlInput: { maxLength: 100 } }}
              required
              fullWidth
            />
          </Stack>
          <Stack direction={{ xs: "column", md: "row" }} spacing={2}>
            <TextField
              label="Телефон"
              value={phone}
              onChange={(event) => setPhone(event.target.value)}
              slotProps={{ htmlInput: { maxLength: 50 } }}
              fullWidth
            />
            <TextField
              label="Должность"
              value={position}
              onChange={(event) => setPosition(event.target.value)}
              slotProps={{ htmlInput: { maxLength: 255 } }}
              fullWidth
            />
          </Stack>
          <FormControl fullWidth>
            <InputLabel id="new-user-role-label">Системная роль</InputLabel>
            <Select
              labelId="new-user-role-label"
              label="Системная роль"
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
            {administration.create.isPending ? "Создание..." : "Создать сотрудника"}
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
              <Button
                color="inherit"
                onClick={() => {
                  setCreatedUser(null);
                  setCopyStatus("idle");
                }}
              >
                Скрыть
              </Button>
            </Stack>
          }
        >
          <Typography sx={{ fontWeight: "bold" }}>
            Временный пароль для {employeeName(createdUser)} ({createdUser.username}).
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
        <Typography variant="h6">Список сотрудников</Typography>
        <Stack direction={{ xs: "column", sm: "row" }} spacing={2}>
          <TextField
            label="Поиск по ФИО, логину, телефону или должности"
            size="small"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            fullWidth
          />
          <FormControlLabel
            sx={{ whiteSpace: "nowrap" }}
            control={
              <Checkbox
                checked={includeArchived}
                onChange={(event) => setIncludeArchived(event.target.checked)}
              />
            }
            label="Показывать архивные"
          />
        </Stack>
      </Stack>

      {isLoading && <Typography>Загрузка сотрудников...</Typography>}
      {isError && (
        <Alert severity="error">
          Не удалось загрузить пользователей. Убедитесь, что у вашей учётной записи есть права администратора.
        </Alert>
      )}
      {!isLoading && !isError && visibleUsers.length === 0 && (
        <Typography color="text.secondary">
          {users?.length ? "По запросу ничего не найдено." : "Пользователи не найдены."}
        </Typography>
      )}

      {visibleUsers.length > 0 && (
        <Paper sx={{ overflowX: "auto" }}>
          <Table size="small" sx={{ minWidth: 1050 }}>
            <TableHead>
              <TableRow>
                <TableCell>Сотрудник</TableCell>
                <TableCell>Телефон</TableCell>
                <TableCell>Должность</TableCell>
                <TableCell>Системная роль</TableCell>
                <TableCell>Статус</TableCell>
                <TableCell>Действия</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {visibleUsers.map((user) => (
                <TableRow key={user.id} hover>
                  <TableCell sx={{ minWidth: 190 }}>
                    <Typography variant="body2" fontWeight={600}>
                      {employeeName(user)}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Логин: {user.username}
                    </Typography>
                  </TableCell>
                  <TableCell sx={{ whiteSpace: "nowrap" }}>
                    {user.phone || "—"}
                  </TableCell>
                  <TableCell>{user.position || "—"}</TableCell>
                  <TableCell sx={{ minWidth: 175 }}>
                    <FormControl
                      size="small"
                      fullWidth
                      disabled={
                        user.archived ||
                        (user.role === "admin" && user.isActive && activeAdminCount <= 1) ||
                        administration.changeRole.isPending
                      }
                    >
                      <Select
                        aria-label={`Системная роль сотрудника ${user.username}`}
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
                  <TableCell sx={{ minWidth: 170 }}>{userStatus(user)}</TableCell>
                  <TableCell>
                    <Stack
                      direction="row"
                      spacing={1}
                      useFlexGap
                      sx={{ flexWrap: "wrap", minWidth: 250 }}
                    >
                      <Button size="small" onClick={() => openProfile(user)}>
                        Сведения
                      </Button>
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
                              if (
                                window.confirm(
                                  `Архивировать пользователя ${user.username}?`,
                                )
                              ) {
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

      <Dialog
        open={editingUser !== null}
        onClose={() => setEditingUser(null)}
        fullWidth
        maxWidth="sm"
      >
        <DialogTitle>Сведения о сотруднике</DialogTitle>
        <form onSubmit={handleProfileSave}>
          <DialogContent>
            <Stack spacing={2} sx={{ pt: 1 }}>
              <Typography variant="body2" color="text.secondary">
                Логин: {editingUser?.username}. Изменение логина здесь не предусмотрено.
              </Typography>
              <TextField
                label="ФИО"
                value={editFullName}
                onChange={(event) => setEditFullName(event.target.value)}
                slotProps={{ htmlInput: { maxLength: 255 } }}
                required
                fullWidth
              />
              <TextField
                label="Телефон"
                value={editPhone}
                onChange={(event) => setEditPhone(event.target.value)}
                slotProps={{ htmlInput: { maxLength: 50 } }}
                fullWidth
              />
              <TextField
                label="Должность"
                value={editPosition}
                onChange={(event) => setEditPosition(event.target.value)}
                slotProps={{ htmlInput: { maxLength: 255 } }}
                fullWidth
              />
            </Stack>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setEditingUser(null)}>Отмена</Button>
            <Button
              type="submit"
              variant="contained"
              disabled={
                !editFullName.trim() || administration.updateProfile.isPending
              }
            >
              {administration.updateProfile.isPending ? "Сохранение..." : "Сохранить"}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Stack>
  );
}
