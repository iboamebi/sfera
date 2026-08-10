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

## Infrastructure Audit

Статус:

COMPLETED

Выполнено:

- Repository implementations audit
- Mapper alignment verification
- UnitOfWork transaction boundary verification
- Dependency direction verification
- WarehouseMovementRepository migration fix

Checkpoint:

- All infrastructure repositories follow DDD repository flow
- No CRUD dependencies remain
- No domain/application dependency violations detected

---

## Infrastructure Mapper Alignment

Статус:

COMPLETED

Выполнено:

- All infrastructure mappers aligned with BaseMapper contract
- Mapper methods standardized:
  - to_domain(self, model)
  - to_model(self, entity, model)
- ORM model creation responsibility removed from mappers where applicable
- Repository layer uses mapper instances consistently

Affected mappers:

- DeviceMapper
- OrderMapper
- PriceListMapper
- MaterialMapper
- WorkflowMapper
- WorkflowStageMapper
- WorkflowInstanceMapper
- VerificationMapper
- RepairMapper
- WarehouseMapper
- WarehouseStockMapper
- WarehouseMovementMapper
- OrganizationMapper
- CustomerMapper
- DiagnosticMapper

Checkpoint:

- Infrastructure mapping layer standardized
- Repository implementations follow unified mapper pattern
- No remaining legacy mapper implementations detected

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

## Checkpoint — 2026-08-05

Architecture Migration: COMPLETE

Completed:
- Workflow migration completed.
- Repository mapper extraction completed.
- PriceListMapper extracted.
- Local repository mapping removed.
- Repository boundaries verified.
- Domain isolation verified.
- Application isolation verified.
- API isolation verified.
- Infrastructure dependency direction verified.

Result:
DDD + Clean Architecture migration completed.

Known architecture technical debt:
None.

---

## Application Services Audit

## Checkpoint — 2026-08-10

Application Services Audit: COMPLETE

Проверены все Application Services:

- Customer
- Device
- Diagnostic
- Material
- Order
- Organization
- PriceList
- Repair
- Verification
- Warehouse
- Workflow

Проверено:

- отсутствие CRUD-style proxy methods;
- отсутствие бизнес-логики в Application layer;
- делегирование state changes в Domain;
- корректность Repository Interface boundaries;
- корректность UnitOfWork transaction boundaries;
- отсутствие Infrastructure/ORM dependencies в Application layer.

Cleanup completed:

- Removed redundant `CustomerApplicationService.save()`.
- Removed redundant `OrganizationApplicationService.save()`.
- Verified no usages of removed `save()` methods.
- Redundant command handlers for device and verification were removed.
- PriceList item update command export was restored.

Результат:

- Application Services выполняют orchestration use cases.
- Domain entities/domain services выполняют бизнес-правила и state transitions.
- Repository operations выполняются через application/domain repository interfaces.
- CRUD-style остатки, обнаруженные в Application Services, удалены.
- No new Application-layer architectural violations detected.

Validation:

- pytest: 26 passed
- ruff check: passed
- ruff format --check: passed

Checkpoint result:

Application layer conforms to current DDD/Clean Architecture rules.

---

## API Layer Audit

## Checkpoint — 2026-08-10

API Layer Audit: COMPLETE

Проверены routers:

- Customer
- Device
- Diagnostic
- Material
- Order
- Organization
- PriceList
- PriceListItem
- Repair
- Verification
- Warehouse
- WarehouseMovement
- WarehouseStock
- Workflow

Также проверен router package `app/api/routers/__init__.py`.

Проверено:

- отсутствие Repository/ORM/Session dependencies в API layer;
- отсутствие Infrastructure dependencies в API layer;
- отсутствие бизнес-логики в routers;
- корректная передача HTTP input в Application Commands/Services;
- корректное mapping Application exceptions → HTTP status codes;
- наличие явных response models там, где контракт уже определён.

Cleanup completed:

- Removed unused `app/api/routers/order_actions.py`.

Результат:

- API layer сохраняет границу `API → Application`.
- Repository и persistence concerns не проникают в routers.
- Business state changes выполняются через Application/Domain layers.
- API audit не выявил новых архитектурных нарушений.

Known API technical debt / follow-up:

- PriceListItem update contract требует отдельной функциональной миграции: текущая schema заявляет `name`, но router не передаёт его в Application command; `service_type` имеет разные semantics в create и update.
- Device connect/disconnect endpoints возвращают структурированные payloads без явной response schema.
- Некоторые create routers генерируют UUID непосредственно в API layer; требуется единая политика генерации identifiers.
- Material update endpoint использует `PUT` с partial-update semantics (`exclude_unset=True`); требует отдельного решения API contract.

Важно:

- Эти пункты не изменялись в рамках API audit.
- PriceListItem contract cleanup должен выполняться отдельным feature/migration этапом, а не смешиваться с архитектурным аудитом.

Validation:

- pytest: 26 passed
- ruff check: passed
- ruff format --check: passed

Checkpoint result:

API layer conforms to current DDD/Clean Architecture dependency rules; identified contract debt is isolated for subsequent incremental work.
