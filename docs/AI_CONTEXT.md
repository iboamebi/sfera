# Sfera Project AI Context

## Project

Sfera is an information system for a service center and metrology laboratory.

Repository:

```text
git@github.com:iboamebi/sfera.git
```

Primary development branch:

```text
develop
```

## Architecture

Sfera follows DDD + Clean Architecture:

```text
Domain → Application → Infrastructure → API
```

Rules:

- API contains transport concerns only;
- Application coordinates use cases;
- Domain owns business state transitions;
- Infrastructure owns persistence, SQLAlchemy repositories and mappers;
- Domain does not import ORM models;
- Domain does not import Infrastructure;
- legacy CRUD/services are not active architectural dependencies;
- no `BaseRouter` usage;
- API create routers do not generate application-owned identifiers.

## Backend Baseline

Python 3.12, FastAPI, PostgreSQL, SQLAlchemy, Alembic, Pydantic and pytest are used by the backend.

The migrated backend modules currently recorded as complete are:

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

## Audit Trail — Current Checkpoint

Date: 2026-09-01

The Audit Trail foundation is implemented.

Application contracts:

```text
AuditOperation
AuditRecord
AuditOperationRepository
AuditRepository
```

Infrastructure:

```text
AuditOperationModel
AuditRecordModel
AuditOperationRepositorySQLAlchemy
AuditRepositorySQLAlchemy
```

Persistence migrations are present for:

- `audit_records`;
- nullable `audit_records.entity_id`;
- `audit_operations`.

Repository dependency providers are present.

The business repository, audit repositories and `UnitOfWork` use the same request-scoped SQLAlchemy session dependency, so current Verification audit persistence participates in the same transaction as the business mutation.

## Verification Audit Integration

`VerificationApplicationService` currently persists audit information for:

```text
approve → verification.approved
reject  → verification.rejected
```

Audit records capture field-level changes and rejection reason where applicable.

Current focused validation:

```text
Verification application tests: 8 passed
Audit/Verification/dependency/infrastructure tests: 14 passed
Ruff: passed for changed audit/dependency files
```

This is **not** system-wide audit completion.

Still open:

- Verification create/archive/correction audit;
- audit coverage of remaining Application mutation points;
- audit read/query API and authorization;
- database-level append-only enforcement;
- explicit system/background actor;
- nested operation correlation;
- retention/archival policy.

See:

```text
docs/architecture/AUDIT_TRAIL.md
docs/architecture/MIGRATION_MATRIX.md
docs/MIGRATION_STATUS.md
```

## Development Protocol

Work in this order:

```text
analyze
→ read current code from GitHub
→ minimal change
→ validate
→ commit/push
→ local validation
→ analyze result
→ next stage
```

Do not assume files, modules, APIs or architecture contracts. Read the actual repository state first.

GitHub analysis/reading should be performed immediately. Stop only when local validation is genuinely required.

After a local validation result, analyze it and continue automatically without repeating completed steps.

## Code Generation

New code must follow the existing project constitution and established DDD/Clean Architecture conventions.

When presenting code for review, provide it sequentially according to the existing project structure, with the file path and a short description, and concise comments for classes/functions where useful.

## Audit Implementation Rule

For an audit-worthy business mutation:

```text
Application use case
    ↓
business mutation
    +
AuditOperation
    +
AuditRecord(s)
    ↓
same UnitOfWork transaction
    ↓
commit
```

Audit persistence must not depend exclusively on post-commit Domain Events.

Generic `UnitOfWork` remains audit-agnostic.

## Next Stage

Before implementing another audit slice, audit the current Application Services and build the system-wide audit-worthy operation matrix. Then implement the next independent mutation slice using the established transactional pattern and synchronize the audit/migration documentation.
