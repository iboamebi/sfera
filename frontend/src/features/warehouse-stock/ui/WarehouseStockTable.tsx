import { Table, TableBody, TableCell, TableHead, TableRow } from "@mui/material";

import type { WarehouseStockRead } from "../model/types";

interface WarehouseStockTableProps {
  items: WarehouseStockRead[];
}

export function WarehouseStockTable({ items }: WarehouseStockTableProps) {
  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>Материал</TableCell>
          <TableCell>Склад</TableCell>
          <TableCell>Количество</TableCell>
          <TableCell>Зарезервировано</TableCell>
          <TableCell>Доступно</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {items.map((item) => (
          <TableRow key={item.id}>
            <TableCell>{item.materialName}</TableCell>
            <TableCell>{item.warehouseName}</TableCell>
            <TableCell>{item.quantity}</TableCell>
            <TableCell>{item.reservedQuantity}</TableCell>
            <TableCell>{item.availableQuantity}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
