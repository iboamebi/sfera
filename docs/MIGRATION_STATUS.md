# Sfera Migration Status

## Current Status

**DDD/Clean Architecture migration is complete for the currently migrated backend modules. Cross-cutting Audit Trail foundation is implemented and Verification approve/reject integration is complete.**

Date: 2026-09-01

## Architecture Baseline

```text
Domain
  ↓
Application
  ↓
Infrastructure
  ↓
API
```

The project follows DDD + Clean Architecture.

Rules remain:

- API contains transport concerns only;
- Application coordinates use cases;
- Domain owns business state transitions;
- Infrastructure owns SQLAlchemy, repositories and mappers;
- Domain does not import ORM/models;
- Domain does not import Infrastructure;
- no active legacy CRUD/services dependencies;
- no `BaseRouter` usage;
- identifier generation for application-owned entities is not performed by API create routers.

## Migrated Modules

The following modules are recorded as migrated/complete:

- Organization
- Customer
- Order
- Material
- Warehouse
- Verification
- Repair
- Diagnostic
- PriceList
- PriceListItem
- Device
- Workflow
- InstrumentType

Migration means that the active application path follows the current Domain → Application → Infrastructure → API boundaries.

## Cross-Cutting Audit Trail

### Foundation complete

Implemented:

- Application `AuditOperation` contract;
- Application `AuditRecord` contract;
- Application audit repository interfaces;
- SQLAlchemy audit persistence models;
- model registry registration;
- Alembic migrations for audit records and audit operations;
- nullable `audit_records.entity_id` migration;
- SQLAlchemy audit repositories;
- repository dependency providers;
- same-request/session wiring with the existing UnitOfWork transaction;
- Verification approve audit persistence;
- Verification reject audit persistence;
- focused application/infrastructure/dependency tests.

### Current Verification coverage

Audit persistence is currently implemented for:

- `verification.approved`;
- `verification.rejected`.

The records capture field-level changes and the rejection reason where applicable.

### Remaining audit work

- system-wide audit-worthy operation matrix;
- audit integration for remaining Verification mutations;
- audit integration for other application mutation points;
- audit read/query API and authorization;
- database-level append-only enforcement;
- explicit system/background actor;
- nested operation correlation;
- retention/archival policy.

## Validation Checkpoint — 2026-09-01

Focused audit/Verification suite:

```text
14 passed
```

Verification application suite:

```text
8 passed
```

Ruff checks for changed audit/dependency files pass.

## Next Stage

Do not treat Audit Trail foundation as system-wide audit completion.

Next sequence:

1. audit current Application Services and identify all mandatory mutation points;
2. create the audit coverage matrix;
3. implement the next mutation slice transactionally;
4. add focused tests;
5. validate;
6. synchronize this document, `docs/architecture/AUDIT_TRAIL.md` and `docs/architecture/MIGRATION_MATRIX.md`.
