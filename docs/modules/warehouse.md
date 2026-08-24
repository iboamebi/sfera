# Модуль Warehouse

**Версия:** 1.1
**Дата актуализации:** 2026-07-16

---

# 1. Назначение

Warehouse реализует управление складским учётом материалов и комплектующих в системе «Сфера».

Модуль обеспечивает:

- хранение информации о материалах;
- учёт остатков;
- регистрацию движений;
- контроль списания и поступления.

---

# 2. Место в бизнес-процессе

Склад обслуживает производственные процессы:

```text
Order

↓

Repair / Verification

↓

Material Usage

↓

Warehouse
```

---

# 3. Основные сущности

## Warehouse

Складское подразделение или место хранения.

---

## Material

Материал или комплектующая.

---

## WarehouseStock

Текущий остаток материала.

---

## WarehouseMovement

История изменения количества.

---

# 4. Структура данных

```text
Warehouse

↓

WarehouseStock

↓

Material

↓

WarehouseMovement
```

---

# 5. Главный принцип учёта

Все изменения остатков выполняются только через:

```text
WarehouseMovement
```

Прямое изменение количества запрещено.

---

# 6. Типы движений

Примеры:

```text
RECEIPT

↓

Поступление
```

```text
CONSUMPTION

↓

Списание
```

```text
RETURN

↓

Возврат
```

```text
TRANSFER

↓

Перемещение
```

---

# 7. Остатки

WarehouseStock хранит текущее состояние:

- склад;
- материал;
- количество.

Источником истории является:

```text
WarehouseMovement
```

---

# 8. Связь с ремонтом

Материалы ремонта списываются:

```text
Repair

↓

WarehouseMovement

↓

WarehouseStock
```

---

# 9. Domain Model

Основные компоненты:

```text
Warehouse Entity

Material Entity

Stock Value Object

WarehouseMovement Entity
```

---

# 10. Application Services

Основной сервис:

```text
WarehouseService
```

Операции:

```text
Add Material

Create Movement

Check Stock

Reserve Material
```

---

# 11. Repository

Интерфейсы:

```text
WarehouseRepository

MaterialRepository

WarehouseMovementRepository
```

Реализация:

```text
SQLAlchemyWarehouseRepository
```

---

# 12. Ограничения

Запрещается:

- создавать отрицательный остаток;
- изменять историю движений;
- удалять движения;
- списывать материалы без основания.

---

# 13. Аудит

Все операции должны быть отслеживаемыми.

Используются:

```text
warehouse_movements

audit_logs
```

---

# 14. Тестирование

Проверяются:

- поступление материалов;
- списание;
- возврат;
- контроль остатков;
- невозможность отрицательного остатка.

---

# 15. Главный принцип

Warehouse является системой учёта движения материальных ресурсов и обеспечивает полную историю изменения складского состояния.
