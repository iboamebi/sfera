import { Fragment, useState } from "react";

import {
  Alert,
  Button,
  Checkbox,
  Chip,
  FormControlLabel,
  Link,
  MenuItem,
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
import { useNavigate } from "react-router";

import { useAssignOrderItemInstrument } from "../add-order-item/model/useAssignOrderItemInstrument";
import { useDeleteOrderItem } from "../add-order-item/model/useDeleteOrderItem";
import { useUpdateOrderItem } from "../add-order-item/model/useUpdateOrderItem";
import { DeviceSelector } from "../add-order-item/ui/DeviceSelector";
import type { OrderItem, OrderItemOperation } from "../model/types";
import { useCreateVerification } from "../../verifications/create-verification/model/useCreateVerification";
import type { VerificationType } from "../../verifications/model/types";

interface OrderItemsProps {
  items: OrderItem[];
  orderId: string;
  customerId: string;
  editable?: boolean;
}

const OPERATION_LABELS: Record<OrderItemOperation, string> = {
  verification: "Поверка",
  diagnostic: "Диагностика",
  repair: "Ремонт",
  sale: "Продажа",
};

const OPERATION_OPTIONS = Object.entries(OPERATION_LABELS) as Array<
  [OrderItemOperation, string]
>;

function getTodayDate(): string {
  const today = new Date();
  const year = today.getFullYear();
  const month = String(today.getMonth() + 1).padStart(2, "0");
  const day = String(today.getDate()).padStart(2, "0");

  return `${year}-${month}-${day}`;
}

const VERIFICATION_TYPE_LABELS: Record<VerificationType, string> = {
  PRIMARY: "Первичная",
  PERIODIC: "Периодическая",
  AFTER_REPAIR: "После ремонта",
};

export function OrderItems({
  items,
  orderId,
  customerId,
  editable = false,
}: OrderItemsProps) {
  const navigate = useNavigate();
  const updateMutation = useUpdateOrderItem(orderId);
  const assignInstrumentMutation = useAssignOrderItemInstrument(orderId);
  const deleteMutation = useDeleteOrderItem(orderId);
  const createVerificationMutation = useCreateVerification(orderId);
  const [editingItemId, setEditingItemId] = useState<string | null>(null);
  const [editedOperations, setEditedOperations] = useState<OrderItemOperation[]>([]);
  const [assigningItemId, setAssigningItemId] = useState<string | null>(null);
  const [selectedInstrumentId, setSelectedInstrumentId] = useState("");
  const [creatingVerificationItemId, setCreatingVerificationItemId] = useState<string | null>(null);
  const [verificationDate, setVerificationDate] = useState(getTodayDate);
  const [verificationType, setVerificationType] = useState<VerificationType>("PRIMARY");
  const [methodology, setMethodology] = useState("");

  const startEditing = (item: OrderItem) => {
    setEditingItemId(item.id);
    setEditedOperations(item.requestedOperations);
  };

  const toggleOperation = (operation: OrderItemOperation) => {
    setEditedOperations((current) =>
      current.includes(operation)
        ? current.filter((value) => value !== operation)
        : [...current, operation],
    );
  };

  const saveEdit = (itemId: string) => {
    updateMutation.mutate(
      { itemId, requestedOperations: editedOperations },
      { onSuccess: () => setEditingItemId(null) },
    );
  };

  const removeItem = (itemId: string) => {
    if (!window.confirm("Удалить позицию заказа?")) {
      return;
    }
    deleteMutation.mutate(itemId);
  };

  const startAssigningInstrument = (item: OrderItem) => {
    setAssigningItemId(item.id);
    setSelectedInstrumentId("");
  };

  const cancelAssigningInstrument = () => {
    setAssigningItemId(null);
    setSelectedInstrumentId("");
  };

  const saveInstrumentAssignment = (itemId: string) => {
    if (!selectedInstrumentId) {
      return;
    }

    assignInstrumentMutation.mutate(
      { itemId, instrumentId: selectedInstrumentId },
      {
        onSuccess: () => {
          setAssigningItemId(null);
          setSelectedInstrumentId("");
        },
      },
    );
  };

  const closeExpandedRow = () => {
    setEditingItemId(null);
    setAssigningItemId(null);
    setCreatingVerificationItemId(null);
    setSelectedInstrumentId("");
  };

  return (
    <Stack spacing={2} sx={{ width: "100%", minWidth: 0 }}>
      <Typography variant="h6">Позиции заказа</Typography>

      {items.length === 0 ? (
        <Typography color="text.secondary" variant="body2">
          Позиции отсутствуют
        </Typography>
      ) : (
        <TableContainer component={Paper} variant="outlined" sx={{ width: "100%" }}>
          <Table size="small" sx={{ minWidth: 1050 }}>
            <TableHead>
              <TableRow>
                <TableCell width={52}>№</TableCell>
                <TableCell>Наименование СИ</TableCell>
                <TableCell>Модель</TableCell>
                <TableCell>Заводской номер</TableCell>
                <TableCell>Тип СИ</TableCell>
                <TableCell>Операции</TableCell>
                <TableCell align="right" width={250}>Действия</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {items.map((item, index) => {
                const expanded =
                  editingItemId === item.id ||
                  assigningItemId === item.id ||
                  creatingVerificationItemId === item.id;

                return (
                  <Fragment key={item.id}>
                    <TableRow hover>
                      <TableCell>{index + 1}</TableCell>
                      <TableCell sx={{ minWidth: 190 }}>
                        {item.instrumentId ? (
                          <Link
                            component="button"
                            type="button"
                            color="primary"
                            underline="hover"
                            sx={{
                              fontWeight: 600,
                              textAlign: "left",
                            }}
                            onClick={() =>
                              navigate(
                                `/devices/${item.instrumentId}?edit=1&returnToOrder=${orderId}`,
                              )
                            }
                          >
                            {item.instrumentName ?? "—"}
                          </Link>
                        ) : (
                          item.instrumentName ?? "—"
                        )}
                        {item.verificationIds.length > 0 && (
                          <Stack direction="row" spacing={0.5} sx={{ flexWrap: "wrap", mt: 0.5 }}>
                            {item.verificationIds.map((verificationId, verificationIndex) => (
                              <Button
                                key={verificationId}
                                size="small"
                                variant="text"
                                sx={{ minWidth: 0, px: 0.5 }}
                                onClick={() => navigate(`/verifications/${verificationId}`)}
                              >
                                Поверка {verificationIndex + 1}
                              </Button>
                            ))}
                          </Stack>
                        )}
                      </TableCell>
                      <TableCell>{item.modification ?? "—"}</TableCell>
                      <TableCell>{item.serialNumber ?? "—"}</TableCell>
                      <TableCell>{item.instrumentTypeName ?? "—"}</TableCell>
                      <TableCell sx={{ minWidth: 150 }}>
                        <Stack direction="row" spacing={0.5} sx={{ flexWrap: "wrap" }}>
                          {item.requestedOperations.map((operation) => (
                            <Chip
                              key={operation}
                              label={OPERATION_LABELS[operation]}
                              size="small"
                            />
                          ))}
                        </Stack>
                        {item.comment && (
                          <Typography color="text.secondary" variant="caption" sx={{ display: "block", mt: 0.5 }}>
                            {item.comment}
                          </Typography>
                        )}
                      </TableCell>
                      <TableCell align="right">
                        <Stack
                          direction="row"
                          spacing={0.5}
                          sx={{
                            flexWrap: "wrap",
                            justifyContent: "flex-end",
                            alignItems: "center",
                          }}
                        >
                          {item.requestedOperations.includes("verification") &&
                            item.instrumentId &&
                            item.verificationIds.length === 0 && (
                              <Button
                                size="small"
                                variant="outlined"
                                onClick={() => {
                                  closeExpandedRow();
                                  setCreatingVerificationItemId(item.id);
                                  setVerificationDate(getTodayDate());
                                  setVerificationType("PRIMARY");
                                  setMethodology("");
                                }}
                              >
                                Создать поверку
                              </Button>
                            )}
                          {editable && !item.instrumentId && (
                            <Button
                              size="small"
                              variant="outlined"
                              onClick={() => {
                                closeExpandedRow();
                                startAssigningInstrument(item);
                              }}
                            >
                              Назначить СИ
                            </Button>
                          )}
                          {editable && (
                            <>
                              <Button
                                size="small"
                                onClick={() => {
                                  closeExpandedRow();
                                  startEditing(item);
                                }}
                              >
                                Изменить
                              </Button>
                              <Button
                                size="small"
                                color="error"
                                disabled={deleteMutation.isPending}
                                onClick={() => removeItem(item.id)}
                              >
                                Удалить
                              </Button>
                            </>
                          )}
                        </Stack>
                      </TableCell>
                    </TableRow>

                    {expanded && (
                      <TableRow key={`${item.id}-details`}>
                        <TableCell colSpan={7} sx={{ py: 2, backgroundColor: "action.hover" }}>
                          <Stack spacing={1.5} sx={{ maxWidth: 720 }}>
                            {creatingVerificationItemId === item.id && (
                              <>
                                <Typography variant="subtitle2">Создание поверки</Typography>
                                <TextField
                                  label="Дата поверки"
                                  type="date"
                                  size="small"
                                  value={verificationDate}
                                  onChange={(event) => setVerificationDate(event.target.value)}
                                  slotProps={{ inputLabel: { shrink: true } }}
                                />
                                <TextField
                                  select
                                  label="Тип поверки"
                                  size="small"
                                  value={verificationType}
                                  onChange={(event) =>
                                    setVerificationType(event.target.value as VerificationType)
                                  }
                                >
                                  {Object.entries(VERIFICATION_TYPE_LABELS).map(([value, label]) => (
                                    <MenuItem key={value} value={value}>
                                      {label}
                                    </MenuItem>
                                  ))}
                                </TextField>
                                <TextField
                                  label="Методика (необязательно)"
                                  size="small"
                                  value={methodology}
                                  onChange={(event) => setMethodology(event.target.value)}
                                />
                                {createVerificationMutation.error && (
                                  <Alert severity="error">
                                    {createVerificationMutation.error.message}
                                  </Alert>
                                )}
                                <Stack direction="row" spacing={1}>
                                  <Button
                                    size="small"
                                    variant="contained"
                                    disabled={createVerificationMutation.isPending || !verificationDate}
                                    onClick={() =>
                                      createVerificationMutation.mutate(
                                        {
                                          orderItemId: item.id,
                                          verificationDate,
                                          verificationType,
                                          methodology,
                                        },
                                        {
                                          onSuccess: (verification) =>
                                            navigate(`/verifications/${verification.id}`),
                                        },
                                      )
                                    }
                                  >
                                    {createVerificationMutation.isPending ? "Создание..." : "Сохранить поверку"}
                                  </Button>
                                  <Button
                                    size="small"
                                    disabled={createVerificationMutation.isPending}
                                    onClick={() => setCreatingVerificationItemId(null)}
                                  >
                                    Отмена
                                  </Button>
                                </Stack>
                              </>
                            )}

                            {assigningItemId === item.id && (
                              <>
                                <Typography variant="subtitle2">Назначение средства измерений</Typography>
                                <DeviceSelector
                                  value={selectedInstrumentId}
                                  customerId={customerId}
                                  instrumentTypeId={item.instrumentTypeId}
                                  onChange={setSelectedInstrumentId}
                                />
                                <Stack direction="row" spacing={1}>
                                  <Button
                                    size="small"
                                    variant="contained"
                                    disabled={assignInstrumentMutation.isPending || !selectedInstrumentId}
                                    onClick={() => saveInstrumentAssignment(item.id)}
                                  >
                                    Назначить СИ
                                  </Button>
                                  <Button
                                    size="small"
                                    disabled={assignInstrumentMutation.isPending}
                                    onClick={cancelAssigningInstrument}
                                  >
                                    Отмена
                                  </Button>
                                </Stack>
                              </>
                            )}

                            {editingItemId === item.id && (
                              <>
                                <Typography variant="subtitle2">Операции по позиции</Typography>
                                <Stack direction="row" sx={{ flexWrap: "wrap" }}>
                                  {OPERATION_OPTIONS.map(([operation, label]) => (
                                    <FormControlLabel
                                      key={operation}
                                      control={
                                        <Checkbox
                                          checked={editedOperations.includes(operation)}
                                          onChange={() => toggleOperation(operation)}
                                        />
                                      }
                                      label={label}
                                    />
                                  ))}
                                </Stack>
                                <Stack direction="row" spacing={1}>
                                  <Button
                                    size="small"
                                    variant="contained"
                                    disabled={updateMutation.isPending || editedOperations.length === 0}
                                    onClick={() => saveEdit(item.id)}
                                  >
                                    Сохранить
                                  </Button>
                                  <Button
                                    size="small"
                                    disabled={updateMutation.isPending}
                                    onClick={() => setEditingItemId(null)}
                                  >
                                    Отмена
                                  </Button>
                                </Stack>
                              </>
                            )}
                          </Stack>
                        </TableCell>
                      </TableRow>
                    )}
                  </Fragment>
                );
              })}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Stack>
  );
}
