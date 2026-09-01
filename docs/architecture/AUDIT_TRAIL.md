# Sfera Audit Trail

## Status

**Foundation implemented. Verification approve/reject integration implemented. System-wide rollout remains open.**

## Date

2026-09-01

## 1. Purpose

The Audit Trail is persistent historical evidence of significant business-state changes. It is separate from Domain Events and must remain available after later changes to the business object.

For an audit-worthy operation it must be possible to determine:

- who initiated the logical operation;
- who directly performed the action;
- when it occurred;
- what changed;
- previous and new values;
- why the change was made when required;
- which logical operation produced the change.

## 2. Architecture

Audit persistence is an Application-layer transactional concern exposed through repository ports.

```text
Application use case
        ↓
Business mutation
        ↓
AuditOperation + AuditRecord(s)
        ↓
Same UnitOfWork / SQLAlchemy transaction
        ↓
COMMIT
```

Failure must roll back the business mutation and its audit records together.

The post-commit Domain Event dispatcher is not the mandatory persistence mechanism for audit records. The generic `UnitOfWork` remains audit-agnostic.

## 3. Identity Model

Direct actor:

```text
AuditRecord.actor_id → User.id
```

Logical operation initiator:

```text
AuditOperation.initiated_by → User.id
```

`AuditOperation.operation_id` correlates all records belonging to one logical operation.

The current Verification implementation uses the authenticated user for both initiator and actor. A dedicated system/background actor remains open.

## 4. Persistence Model

### AuditOperation

```text
operation_id UUID PRIMARY KEY
initiated_by  UUID NOT NULL
```

### AuditRecord

```text
id                 UUID PRIMARY KEY
operation_id       UUID NOT NULL
actor_id           UUID NOT NULL
action             VARCHAR(100) NOT NULL
entity_type        VARCHAR(100) NOT NULL
entity_id          UUID NULL
changes            JSONB NOT NULL
reason             VARCHAR(1000) NULL
related_record_id  UUID NULL → audit_records.id
occurred_at        timestamptz NOT NULL DEFAULT now()
```

`entity_id` is nullable because an audit record may concern a logical operation rather than one persisted entity.

`occurred_at` is authoritative database time and is not part of the Application `AuditRecord` constructor.

## 5. Change Representation

Field-level changes use stable JSON-compatible values:

```json
{
  "status": {
    "old": "PENDING",
    "new": "APPROVED"
  }
}
```

UUIDs and datetimes are serialized as strings, enums use stable values, and `None` is JSON `null`.

Passwords, tokens, credentials and other secrets must never be captured automatically.

## 6. Stable Action Identifiers

`action` and `entity_type` are application-level stable identifiers and must not depend on ORM or Python class names.

The intended convention is:

```text
<entity>.<operation>
```

Examples include `verification.approved`, `verification.rejected`, `order.created`, `workflow.started` and `workflow.completed`.

Existing Verification records currently use the established `Verification` entity type and must retain that value for compatibility.

## 7. Verification Integration

Audit-worthy Verification operations are:

- create;
- approve;
- reject;
- archive;
- correction of erroneous or unreliable data.

Currently persisted by `VerificationApplicationService`:

- `verification.approved`;
- `verification.rejected`.

Approve/reject records capture the changes to `result`, `valid_until` and `unsuitable_reason`; rejection also records the supplied reason.

Create, archive and correction remain open implementation items.

## 8. Transaction Boundary

The existing dependency graph supplies the business repository, audit repositories and `UnitOfWork` from the same request-scoped SQLAlchemy session dependency.

```text
get_session()
 ├── business repository
 ├── AuditRepositorySQLAlchemy
 └── AuditOperationRepositorySQLAlchemy
          ↓
   SqlAlchemyUnitOfWork
          ↓
    commit / rollback
```

No audit-specific API has been added to the generic UnitOfWork contract.

## 9. Immutability

Audit history is append-only:

```text
INSERT
  ↓
never UPDATE
never DELETE
```

The current repository contracts expose persistence through `save()` only. Database-level UPDATE/DELETE protection remains a production hardening task.

Corrections must be represented by new records using `related_record_id`; the original record remains unchanged.

## 10. Separation from Domain Events

Domain Events coordinate application behavior and are dispatched after the database transaction. Audit records provide mandatory persistent accountability history.

A Domain Event alone does not satisfy the Audit Trail requirement.

## 11. Architectural Boundaries

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

Audit repository interfaces belong to the Application layer. SQLAlchemy implementations belong to Infrastructure.

Prohibited:

- SQLAlchemy in Domain;
- database access from API routers;
- audit logic in legacy CRUD;
- mandatory audit persistence only in post-commit handlers;
- audit-specific knowledge in generic UnitOfWork.

## 12. Implemented Foundation

Implemented:

- immutable Application `AuditOperation` contract;
- immutable Application `AuditRecord` contract;
- Application repository interfaces;
- SQLAlchemy persistence models;
- model registry registration;
- Alembic migrations for audit records, nullable `entity_id`, and audit operations;
- SQLAlchemy repositories;
- repository dependency providers;
- Verification approve/reject audit persistence;
- field-level change capture for approve/reject;
- shared UnitOfWork transaction boundary;
- application, infrastructure and dependency tests for the implemented foundation.

## 13. Remaining Work

- system-wide audit coverage matrix and rollout;
- Verification create/archive/correction integration;
- audit read/query contract and API;
- database-level append-only enforcement;
- explicit system/background actor representation;
- operation propagation across nested use cases;
- retention and archival policy;
- authorization policy for audit read access.

## 14. Validation — 2026-09-01

Current focused audit/Verification validation:

```text
14 passed
```

Verification application suite:

```text
8 passed
```

Ruff checks for the changed audit/dependency files pass.

## 15. Next Stage

Do not expand Verification further before auditing the remaining Application mutation points.

Next sequence:

1. build the system-wide audit-worthy operation matrix from current Application Services;
2. select the next independent mutation slice;
3. add `AuditOperation` + `AuditRecord` within the same UnitOfWork transaction;
4. add focused tests;
5. validate and update this document and the migration documentation.
