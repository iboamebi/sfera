# Sfera Migration Matrix

Date: 2026-09-01

## Status Legend

- **COMPLETED** — active path follows the target DDD/Clean Architecture boundary and focused validation exists.
- **PARTIAL** — foundation exists, but the migration/rollout is not complete.
- **OPEN** — not yet implemented or not yet audited.

## Backend Modules

| Module | Status | Current boundary |
|---|---|---|
| Organization | COMPLETED | Domain → Application → Infrastructure → API |
| Customer | COMPLETED | Domain → Application → Infrastructure → API |
| Order | COMPLETED | Domain → Application → Infrastructure → API |
| Material | COMPLETED | Domain → Application → Infrastructure → API |
| Warehouse | COMPLETED | Domain → Application → Infrastructure → API |
| Verification | COMPLETED | Domain → Application → Infrastructure → API |
| Repair | COMPLETED | Domain → Application → Infrastructure → API |
| Diagnostic | COMPLETED | Domain → Application → Infrastructure → API |
| PriceList | COMPLETED | Domain → Application → Infrastructure → API |
| PriceListItem | COMPLETED | Domain → Application → Infrastructure → API |
| Device | COMPLETED | Domain → Application → Infrastructure → API |
| Workflow | COMPLETED | Domain → Application → Infrastructure → API |
| InstrumentType | COMPLETED | Domain → Application → Infrastructure → API |

`COMPLETED` describes architectural migration of the module. It does not imply that every cross-cutting concern is implemented for every use case.

## Cross-Cutting Audit Trail

| Area | Status | Notes |
|---|---|---|
| AuditOperation Application contract | COMPLETED | Immutable Application model |
| AuditRecord Application contract | COMPLETED | Immutable Application model |
| Audit repository ports | COMPLETED | Application layer |
| SQLAlchemy audit models | COMPLETED | Infrastructure persistence models |
| Model registry | COMPLETED | Audit models registered |
| Alembic audit_records migration | COMPLETED | Persistent audit record table |
| Nullable audit entity_id migration | COMPLETED | Supports operation-level records |
| Alembic audit_operations migration | COMPLETED | Logical operation correlation |
| SQLAlchemy audit repositories | COMPLETED | Infrastructure implementations |
| Repository DI | COMPLETED | Providers use the current session boundary |
| Transactional Verification audit | PARTIAL | Approve/reject implemented |
| System-wide audit coverage | OPEN | Mutation matrix still required |
| Verification create/archive/correction audit | OPEN | Not yet integrated |
| Audit read/query API | OPEN | No read contract/API yet |
| Append-only DB enforcement | OPEN | Production hardening remains |
| System/background actor | OPEN | Explicit representation remains |
| Nested operation propagation | OPEN | Correlation policy remains |
| Retention/archival policy | OPEN | Operational policy remains |

## Verification Audit Slice

Currently implemented mutations:

```text
VerificationApplicationService
    ├── approve → AuditOperation + AuditRecord
    └── reject  → AuditOperation + AuditRecord
```

The business mutation and audit persistence use the same UnitOfWork transaction.

Current focused validation:

```text
8 Verification application tests passed
14 focused audit/Verification/dependency/infrastructure tests passed
```

## Architectural Constraints

The matrix must not be interpreted as permission to bypass the project constitution.

Required direction:

```text
API
 ↓
Application
 ↓
Domain / repository contracts
 ↑
Infrastructure
 ↓
Database
```

Audit repositories are Application ports; SQLAlchemy implementations remain in Infrastructure. Generic UnitOfWork remains unaware of audit-specific behavior.

## Next Migration/Audit Stage

1. Audit current Application Services for significant mutation points.
2. Build a system-wide audit coverage matrix.
3. Implement the next independent mutation slice transactionally.
4. Validate with focused tests and the relevant broader suite.
5. Synchronize `AUDIT_TRAIL.md`, this matrix and `MIGRATION_STATUS.md`.
