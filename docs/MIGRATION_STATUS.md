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

IN_PROGRESS

Выполнено:

- Domain entity
- Repository interface
- SQLAlchemy repository
- Application Service
- Dependency Injection
- API Router migration
- Architecture documentation

Осталось:

- Синхронизация Domain модели и SQLAlchemy модели
- Alembic migration
- Проверка Repository integration
- Тесты Application Service
- API тесты
- Удаление legacy CRUD зависимости

PriceList используется как эталонный модуль перехода CRUD → DDD.

---

## Следующие кандидаты миграции

Порядок:

1. PriceList
2. Customer
3. Order
4. Material
5. Warehouse
6. Verification
7. Repair
8. Diagnostic

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

2026-07-29

Baseline:

Sfera Architecture v2.0

Завершено:

- Архитектурные стандарты
- Project Constitution
- Layer Standards
- Начата миграция PriceList

Следующий этап:

Завершить PriceList.

После этого продолжить миграцию модулей по очереди.
