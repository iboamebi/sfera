# Sfera Migration Status

## Текущая задача

Переход от CRUD-архитектуры к DDD/Clean Architecture.

## Текущая схема

API
→ CRUD
→ SQLAlchemy Model

## Целевая схема

API
→ Application Service
→ Repository Interface
→ Infrastructure Repository
→ Database

---

## Статус миграции модулей

### Organization

Статус:

COMPLETED

Выполнено:

- Domain entity
- Repository interface
- SQLAlchemy repository
- Application Service
- Dependency Injection
- API migration

---

### PriceList

Статус:

COMPLETED

Выполнено:

- Domain entity
- Repository interface
- SQLAlchemy repository
- Application Service
- Dependency Injection
- API Router migration
- Architecture documentation

Legacy implementation archived:

- docs/archive/legacy_price_list/

Осталось:

- Удаление legacy CRUD зависимости выполнено
- Миграция завершена

PriceList использовался как эталонный модуль перехода CRUD → DDD.

---

### Customer

Статус:

COMPLETED

Выполнено:

- Domain entity
- Domain exceptions
- Repository interface
- SQLAlchemy repository
- Mapper
- CreateCustomerCommand
- UpdateCustomerCommand
- Application Service migration
- API Router migration
- Domain state change methods
- Tests validation

Checkpoint:

- Customer application flow migrated to DDD commands
- API no longer contains update logic

---

## Следующие кандидаты миграции

Порядок:

1. Customer ✅
2. Order
3. Material
4. Warehouse
5. Verification
6. Repair
7. Diagnostic

---

## Правила миграции

Во время перехода:

- Legacy CRUD используется только как источник текущей бизнес-логики.
- Новые функции реализуются только через DDD/Clean Architecture.
- Бизнес-логика не добавляется в CRUD.
- Каждый модуль мигрируется по схеме:

Domain
↓
Application Service
↓
Repository Interface
↓
Infrastructure Repository
↓
API

---

## Текущий архитектурный checkpoint

Дата:

2026-07-30

Baseline:

Sfera Architecture v2.0

Завершено:

- Архитектурные стандарты
- Project Constitution
- Layer Standards
- PriceList DDD migration
- Legacy PriceList implementation archived
- Customer DDD migration

Следующий этап:

Миграция Order по стандартной схеме.

После этого продолжить миграцию модулей по очереди.
