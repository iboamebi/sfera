# Sfera Migration Matrix

| Module | Legacy | Domain | Application Service | Repository | Infrastructure | API | Exceptions | Status |
|--------|--------|--------|---------------------|------------|----------------|-----|------------|--------|
| Organization | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED |
| Customer | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED |
| Order | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED |
| Material | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED |
| Warehouse | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED |
| Verification | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED |
| Repair | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED |
| Diagnostic | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED |
| PriceList | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED* |
| PriceListItem | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED* |
| Device | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED |
| Workflow | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED |

`*` Migration is complete. PriceList / PriceListItem have an isolated identifier-creation contract debt that must be resolved separately.

---

# Current Architecture

```text
API
↓
Application Service
↓
Domain
↓
Repository Interface
↑
Infrastructure Repository
↓
Database
```

---

# Migration Standard

Каждый новый функционал реализуется исключительно через Application use case и repository abstraction:

```text
API
↓
Application Service / Command
↓
Domain
↓
Repository Interface
↑
Infrastructure Repository
↓
Database
```

Правила:

- Domain не зависит от внешних слоев.
- Application не зависит от Infrastructure.
- API не содержит бизнес-логику.
- API не обращается к Repository или Database напрямую.
- SQLAlchemy используется только в Infrastructure.
- Legacy CRUD запрещён для новых use cases.
- Новые use cases создаются через Application Services.
- Domain state changes принадлежат Domain entities/domain services.
- Infrastructure отвечает за persistence и mapping.

---

# Completed Architecture Checkpoints

## DDD/Clean Architecture

Status:

COMPLETED

Completed:

- Domain isolation
- Application isolation
- Infrastructure isolation
- API migration
- Repository abstraction
- Legacy CRUD removal
- Device migration
- Workflow migration
- PriceList migration

Validation:

- pytest: 33 passed
- ruff check: passed
- ruff format --check: passed

---

## Application Services Audit

Status:

COMPLETED

Completed:

- Application Service dependency audit
- CRUD-style operation audit
- Domain state-change delegation audit
- Repository interface boundary audit
- UnitOfWork transaction boundary audit
- Infrastructure dependency isolation

Result:

- Application Services coordinate use cases.
- Business state transitions remain in Domain.
- Repository access uses repository interfaces.
- No new Application-layer architecture violations detected.

Validation:

- pytest: 33 passed
- ruff check: passed
- ruff format --check: passed

---

## API Layer Audit

Status:

COMPLETED

Completed:

- API dependency isolation
- Repository/ORM/Session isolation
- Infrastructure dependency isolation
- Business-logic isolation
- Application Command/Service boundary verification
- Application exception to HTTP boundary verification
- API router cleanup

Identifier generation cleanup:

- UUID generation removed from create routers.
- API routers no longer generate entity identifiers.
- Identifier generation is handled by the Application layer for simple entity creation.

Known isolated API contract debt:

- PriceListItem update contract requires a separate functional migration.
- Device connect/disconnect endpoints lack explicit response schemas.
- Material update endpoint uses `PUT` with partial-update semantics.

Validation:

- pytest: 33 passed
- ruff check: passed
- ruff format --check: passed

---

## Identifier Generation Audit

Status:

COMPLETED

Scope:

- API routers
- Application Services
- Domain entities
- Domain factories
- Domain `create()` methods

Result:

- API UUID generation removed.
- Application layer owns identifier generation for simple entity creation.
- Domain factories may generate identifiers when they construct complete domain structures.
- Domain `create()` methods receive identifiers explicitly where identifier generation is not itself a domain business rule.
- No new architecture violations found in Customer, Organization, Material, Warehouse, Order, Workflow, Diagnostic, Repair and Device creation flows.

Known technical debt:

- `PriceList.create()` does not currently accept or assign an identifier.
- `PriceListItem` creation does not currently provide an identifier.
- PriceList application test coverage is absent.

Validation:

- pytest: 33 passed
- ruff check: passed
- ruff format --check: passed

---

## Domain Exceptions Isolation

Status:

COMPLETED

Completed:

- Specialized domain exceptions
- Generic ValueError removed from migrated domain logic
- Domain validation boundaries isolated

Modules:

- Device
- Order
- Verification
- Warehouse

Validation:

- Domain has no ORM dependencies
- Domain has no Infrastructure dependencies
- pytest: 33 passed

---

## Infrastructure Mapper Alignment

Status:

COMPLETED

Completed:

- Mapper contract alignment
- `to_domain()` standardization
- `to_model()` standardization
- Repository/mapper integration
- PriceListMapper extraction
- Legacy mapper implementations removed

Validation:

- Infrastructure repositories use mapper abstractions
- Domain remains isolated from ORM
- pytest: 33 passed
- ruff check: passed

---

## Architecture Dependency Audit

Status:

COMPLETED

Completed:

- Clean Architecture dependency verification
- API layer isolation verification
- Application layer isolation verification
- Domain layer isolation verification
- Repository interface boundary verification
- Infrastructure dependency direction verification
- Legacy CRUD dependency verification

Validation:

- API contains no repository dependencies
- Application contains no Infrastructure dependencies
- Domain contains no ORM dependencies
- Infrastructure contains no API/Application dependencies
- pytest: 33 passed

---

## Order Domain Events Foundation

Status:

COMPLETED

Scope:

- AggregateRoot event collection
- DomainEvent base contract
- OrderRegistered event
- UnitOfWork event collection and dispatch
- EventDispatcher integration
- operation-to-event correlation

Result:

- `AggregateRoot` collects domain events and exposes them through `collect_events()`.
- `Order.register()` produces `OrderRegistered`.
- `SqlAlchemyUnitOfWork` dispatches collected domain events after a successful database commit.
- `OperationContext.operation_id` is propagated to the event through the UnitOfWork boundary.
- `EventDispatcher` dispatches events to registered handlers.
- Persistent Audit Trail foundation and the first transactional Verification integration slice are implemented; system-wide audit coverage remains open.

Validation:

- Order domain-event foundation tests: 3 passed

---

# Current Checkpoint — 2026-08-31

The DDD/Clean Architecture migration and the main architecture audits are complete.

Completed:

- DDD/Clean Architecture migration
- Application Services audit
- API Layer audit
- Identifier Generation audit
- Infrastructure mapper alignment
- Legacy CRUD removal
- Architecture dependency validation
- Order domain events foundation
- Order operation-to-event correlation

Open technical debt is intentionally isolated from completed migration work:

1. PriceList / PriceListItem identifier creation contract.
2. PriceList application test coverage.
3. Existing API contract debt listed in the API Layer Audit.
4. Workflow orchestration after event and audit contracts are finalized.

Current direction:

```text
Persistent Audit Trail foundation
        ↓
system-wide audit coverage review
        ↓
workflow orchestration
```

Feature migration and architectural cleanup must remain separate changes.
