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
- Mapper
- Application Service
- Dependency Injection
- API migration
- Schemas migration

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

### Order

Статус:

COMPLETED

Выполнено:

- Domain entity
- Value Objects
- Repository interface
- SQLAlchemy repository
- Mapper
- Application services
- Commands
- API migration

---

### Material

Статус:

COMPLETED

Выполнено:

- Domain entity
- Repository interface
- SQLAlchemy repository
- Mapper
- Application Service
- API migration

---

### Warehouse

Статус:

COMPLETED

Выполнено:

- Domain entities
- Value Objects
- Repository interfaces
- SQLAlchemy repositories
- Application services
- API migration

---

### Verification

Статус:

COMPLETED

Выполнено:

- Domain entity
- Value Objects
- Repository interface
- SQLAlchemy repository
- Mapper
- Application Service
- Commands
- API migration

---

### Repair

Статус:

COMPLETED

Выполнено:

- Domain entity
- Value Objects
- Repository interface
- SQLAlchemy repository
- Mapper
- Application Service
- Commands
- API migration

---

### Diagnostic

Статус:

COMPLETED

Выполнено:

- Domain entity
- Repository interface
- SQLAlchemy repository
- Mapper
- Application Service
- Commands
- API Router
- Schemas
- Legacy CRUD archived

---

## Legacy CRUD

Статус:

ARCHIVED

Правила:

- Legacy CRUD используется только как источник текущей бизнес-логики.
- Новые функции через CRUD не добавляются.
- Новые изменения выполняются только через DDD/Clean Architecture.

---

## Архитектурный checkpoint

Дата:

2026-08-01

Baseline:

Sfera Architecture v2.0

Завершено:

- Project Constitution
- Architecture Standards
- Layer Standards
- PriceList DDD migration
- Organization DDD migration
- Customer DDD migration
- Order DDD migration
- Material DDD migration
- Warehouse DDD migration
- Verification DDD migration
- Repair DDD migration
- Diagnostic DDD migration

---

## Следующий этап

Провести анализ оставшихся модулей:

- определить следующий кандидат миграции;
- проверить зависимости;
- подготовить вертикальный DDD срез.

Перед началом следующей миграции:

1. Проверить структуру существующего модуля.
2. Сравнить с эталонными DDD модулями.
3. Выполнить миграцию:

Domain
↓
Application Service
↓
Repository Interface
↓
Infrastructure Repository
↓
API
↓
Tests
