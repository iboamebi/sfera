import { useState } from "react";
import { Alert, Button, Dialog, DialogActions, DialogContent, DialogTitle, Stack, TextField } from "@mui/material";
import { useMutation } from "@tanstack/react-query";
import { cancelVerification } from "../api/cancelVerification";
interface Props { verificationId: string; requireReason: boolean; onCancelled: () => void; }
export function CancelVerificationButton({ verificationId, requireReason, onCancelled }: Props) {
 const [open,setOpen]=useState(false); const [reason,setReason]=useState("");
 const mutation=useMutation({mutationFn:()=>cancelVerification({verificationId,...(reason.trim()?{reason:reason.trim()}:{})}),onSuccess:onCancelled});
 return <Stack spacing={1}>{mutation.error&&<Alert severity="error">{mutation.error.message}</Alert>}<Button color="error" variant="outlined" onClick={()=>setOpen(true)}>Отменить поверку</Button><Dialog open={open} onClose={()=>!mutation.isPending&&setOpen(false)} fullWidth maxWidth="sm"><DialogTitle>Отмена поверки</DialogTitle><DialogContent><TextField autoFocus fullWidth multiline minRows={3} margin="dense" label={requireReason?"Причина отмены (обязательно)":"Причина отмены (необязательно)"} value={reason} onChange={e=>setReason(e.target.value)}/></DialogContent><DialogActions><Button onClick={()=>setOpen(false)} disabled={mutation.isPending}>Назад</Button><Button color="error" variant="contained" disabled={mutation.isPending||(requireReason&&!reason.trim())} onClick={()=>mutation.mutate()}>Подтвердить отмену</Button></DialogActions></Dialog></Stack>;
}
