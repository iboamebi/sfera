# Sfera Migration Status

## Текущая задача

Переход от CRUD-архитектуры к DDD/Clean Architecture.

## Текущая схема

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

---

### PriceList

Статус:

COMPLETED

Выполнено:

- Domain entity
- Repository interface
- Infrastructure repository
- Repository mapping implemented
- Application Service
- Commands
- PriceListItem migration
- API Router migration
- Dependency Injection

Checkpoint:

- PriceList migrated to DDD flow
- Legacy PriceList service removed
- Legacy CRUD dependency removed

---

### Workflow

Статус:

COMPLETED

Выполнено:

- Domain entities
- Repository interfaces
- SQLAlchemy repositories
- WorkflowMapper
- WorkflowStageMapper
- WorkflowInstanceMapper
- WorkflowApplicationService
- StartWorkflowCommand
- MoveWorkflowStageCommand
- CompleteWorkflowCommand
- API migration
- Dependency Injection
- Workflow tests
- Architecture tests

Checkpoint:

- Workflow migrated to DDD application flow
- Workflow stages loaded in repository using `selectinload`
- Workflow persistence mapping moved to Infrastructure
- Workflow commands fully replace legacy flow

---

## Legacy Layers

Статус:

REMOVED

Удалено:

- `app/crud`
- `app/services/price_list_service.py`
- `app/api/base_router.py`

Проверки:

- No active imports from `app.crud`
- No active imports from `app.services`
- No BaseRouter usage

---

## Domain Layer Isolation

Статус:

COMPLETED

Выполнено:

- Removed ORM imports from Domain layer
- Removed Infrastructure imports from Domain layer
- Domain factories create only domain entities
- ORM mapping moved to Infrastructure layer

Проверки:

- No imports from `app.models` in `app/domains`
- No imports from `app.infrastructure` in `app/domains`
- pytest: 26 passed

---

## Architecture Audit

Статус:

COMPLETED

Проверено:

- Legacy dependency audit
- Domain layer dependency isolation
- Application layer dependency isolation
- API layer isolation
- Infrastructure dependency direction
- Repository interface boundaries
- Mapper consistency audit

Результаты:

- No active imports from `app.crud`
- No active imports from `app.services`
- No BaseRouter usage
- Domain has no ORM dependencies
- Domain has no Infrastructure dependencies
- Application has no Infrastructure dependencies
- Application has no ORM dependencies
- API has no Repository dependencies
- API has no Session dependencies
- Infrastructure has no API/Application dependencies

Technical debt found:

- PriceList repository contains local `_to_domain()` mapping
- PriceList mapper extraction required for full mapper consistency

Audit checkpoint:

- DDD/Clean Architecture dependency rules validated
- Workflow migration architecture validated
- Remaining technical debt isolated

---

## Architecture Audit
