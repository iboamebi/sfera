# Sfera Audit Trail

## Status

Architecture decision recorded. Implementation is not yet introduced.

## Date

2026-08-26

## Scope

This document records the audit requirements and architectural decisions established during the production-readiness audit of Verification and the comparison with the current Sfera architecture.

The document describes the required audit mechanism based on the current code. It does not treat future implementation as already existing.

---

## 1. Business Requirement

Sfera is used by multiple users. For every significant business change it must remain possible to determine:

- who initiated the operation;
- who directly performed each action;
- when it was performed;
- what changed;
- what the previous value was;
- what the new value became;
- why the change was made when a reason is required;
- which operation produced the change.

The historical chain must remain available after later changes to the business object.

The operational requirement is:

> It must always be possible to trace the responsible user at the end of a business-change chain.

---

## 2. Current Implementation Finding

The current code contains Domain Events and an EventDispatcher, but they are not a persistent audit journal.

Current event flow:

```text
Aggregate
    ↓
collect events
    ↓
UnitOfWork
    ↓
commit
    ↓
EventDispatcher
    ↓
Handlers
```

Domain event dispatch occurs after the database commit. Therefore a mandatory audit record must not depend exclusively on the current Domain Event dispatcher.

The current `UnitOfWork` provides the application transaction abstraction. However, the exact SQLAlchemy session wiring and concrete transaction implementation must still be verified from the current Infrastructure/dependency code before audit persistence is implemented.

---

## 3. Architectural Decision: Audit Is a Transactional Persistence Concern

Business mutation and its mandatory audit record must be committed atomically.

Required flow:

```text
Application Use Case
        ↓
 business mutation
        ↓
 audit operation + audit record(s)
        ↓
 same UnitOfWork / transaction
        ↓
      COMMIT
```

On failure:

```text
business mutation + audit record(s)
        ↓
      ROLLBACK
```

The current post-commit Domain Event dispatcher must not be treated as the sole persistence mechanism for mandatory audit records.

Audit-specific APIs must not be added to the generic `UnitOfWork` merely to support auditing. Audit persistence must use the same transaction/session boundary established by the application transaction mechanism.

---

## 4. Actor Identity and Operation Initiation

The audit mechanism distinguishes the initiator of a logical operation from the direct actor of an individual audit action.

### Direct actor

```text
AuditRecord.actor_id → User.id
```

`actor_id` identifies the authenticated user or technical/system actor that directly performed the recorded action.

`username` is not the historical identity key.

### Operation initiator

A logical application operation may produce multiple audit records and may involve a background/system actor. Therefore the operation itself has an initiator:

```text
AuditOperation.initiated_by → User.id / system actor
```

Examples:

```text
User action:
    initiated_by = User A
    actor_id     = User A

Background processing initiated by a user:
    initiated_by = User A
    actor_id     = SYSTEM

Pure system operation:
    initiated_by = SYSTEM
    actor_id     = SYSTEM
```

No anonymous audit operation is permitted.

Authentication/session details must not enter the Domain model merely to support audit. The Domain remains independent from FastAPI, HTTP sessions and authentication infrastructure.

The distinction between `initiated_by` and `actor_id` is required so that a background or automated action does not hide the original initiator.

---

## 5. Audit-Worthy Operations

Audit is mandatory for operations that create, modify, archive, restore or otherwise change significant business state.

The minimum system rule is:

> Every significant business-state change or significant creation/archive/correction operation must leave an immutable audit record.

Read-only operations are not included by default. Auditing data access is a separate future business/security requirement.

### Verification

The following operations are audit-worthy:

- create verification;
- approve verification;
- reject verification;
- archive verification;
- correction of erroneous or unreliable data.

`reject` requires a reason according to the Verification business rule.

Archive/correction actions must preserve the previous history rather than replacing it.

---

## 6. Verification History Rule

Verification history must never be physically deleted.

The current business rule is:

```text
Current relevant result
    = latest successfully completed verification
```

During an active set of current verifications, multiple verification records may exist. Until one successful verification is established as the applicable result, the competing records remain historical records. Once a later decision is established, the latest applicable decision has higher priority.

An older verification record is not deleted because a newer result becomes applicable.

Incorrect or unreliable data follows this flow:

```text
incorrect / unreliable data
        ↓
mark as invalid / archived
        ↓
record reason / basis
        ↓
retain original record
        ↓
create correction separately
```

The history must retain who, when and why.

The same principle applies to the audit journal itself: an audit record that is later found to be incorrect is never rewritten or deleted. Its invalidation or correction is represented by a new audit record.

---

## 7. Audit Operation and Record Model

One logical application operation is represented by an `AuditOperation`. Individual changes produced by that operation are represented by `AuditRecord` entries.

Conceptual model:

```text
AuditOperation
├── operation_id
└── initiated_by

AuditRecord
├── id
├── operation_id
├── actor_id
├── occurred_at
├── action
├── entity_type
├── entity_id
├── changes
├── reason
└── related_record_id
```

`operation_id` is shared by all records belonging to one logical application operation.

`AuditRecord.id` identifies one historical record and is distinct from `operation_id`.

`operation_id` is not unique across audit records.

---

## 8. Identifier Rules

Both `AuditOperation.operation_id` and `AuditRecord.id` are UUIDs.

The approved generation boundary is the Application layer:

```text
Application
 ├── operation_id = UUID
 └── audit record id = UUID
```

The database remains responsible for persistence constraints, but not for the semantic generation of these application identifiers.

Required lookup indexes are:

```text
INDEX(operation_id)
INDEX(entity_type, entity_id)
INDEX(occurred_at)
```

The exact physical index names and migration details remain implementation concerns.

---

## 9. Audit Record Format

The approved representation is **field-level changes**, not full-object snapshots for every mutation.

The conceptual persistence contract is:

```text
AuditRecord
├── id                 UUID PK
├── operation_id       UUID NOT NULL
├── actor_id           UUID NOT NULL
├── occurred_at        timestamptz NOT NULL DEFAULT now()
├── action             stable string
├── entity_type        stable string
├── entity_id          UUID
├── changes            JSONB
├── reason             nullable
└── related_record_id  nullable FK → AuditRecord.id
```

### `changes`

`changes` is stored as PostgreSQL `JSONB`.

The primary shape is:

```json
{
  "status": {
    "old": "PENDING",
    "new": "APPROVED"
  }
}
```

Only business fields that actually changed are recorded.

Values must be represented in a JSON-compatible stable form:

- UUID → string;
- datetime → ISO-8601 string;
- Enum → stable enum value;
- `None` → JSON `null`;
- primitive JSON-compatible values → unchanged.

Sensitive technical data such as passwords, tokens, credentials and secrets must never be captured automatically.

### Lifecycle operations

`create` records relevant `null → new` values.

`update` records only changed `old → new` values.

`archive` records the relevant state transition, for example `archived: false → true`.

Physical deletion is not the normal mechanism for audit-worthy business history. Where business policy requires removal from the active state, an archival/state transition is used instead.

Full ORM snapshots are not stored automatically. A full snapshot requires separate explicit business justification.

---

## 10. Stable `entity_type`

`entity_type` is a stable application-level string.

Examples:

```text
verification
order
device
workflow
instrument
customer
```

It must not be derived from Python class names, ORM class paths or implementation details.

Historical audit records retain their original `entity_type` even if internal class names change.

`entity_id` identifies the specific business object.

---

## 11. Stable `action`

`action` is a stable application-level string identifying the business operation.

The convention is:

```text
<entity_type>.<operation>
```

Examples:

```text
verification.created
verification.approved
verification.rejected
verification.archived
verification.corrected

order.created
workflow.started
workflow.completed
```

`action` is not a global enum and does not depend on Python method names.

A new business operation receives a new stable action identifier.

---

## 12. `reason` Policy

`reason` is nullable in the common `AuditRecord` persistence contract because different business operations have different requirements.

Whether `reason` is mandatory is a rule of the concrete Application use case.

For Verification, the current decisions are:

```text
verification.approved   → reason optional
verification.rejected   → reason required
verification.archived   → reason required
verification.corrected  → reason required
```

The requirement must be enforced by the corresponding Application command/use case, not by a global audit registry.

`reason` is the explicit basis for the operation and must not be silently generated by Infrastructure.

---

## 13. Audit Record Immutability and Corrections

Audit Trail is append-only.

The intended rule is:

```text
INSERT audit record
    ↓
never UPDATE
never DELETE
```

No `archived` flag is used to hide or replace an audit record.

If an audit record is discovered to contain incorrect or unreliable information, the original record remains unchanged. A new audit record documents the invalidation or correction.

The approved relationship is:

```text
AuditRecord A
    ↓
AuditRecord B
    action = verification.corrected
    related_record_id = A.id
```

or, for invalidation:

```text
AuditRecord A
    ↓
AuditRecord B
    action = audit.record.invalidated
    related_record_id = A.id
```

`related_record_id` is deliberately neutral. It is interpreted together with the stable `action` rather than pretending that every relationship is a replacement/supersession.

For the current Verification scope, one new corrective/invalidation record refers to one prior audit record. A multi-record correction relation is outside the current scope and must be designed separately if required.

Database-level protection against `UPDATE`/`DELETE` is required in production in addition to an append-only Repository contract.

---

## 14. Timestamp Rule

`occurred_at` is the authoritative audit timestamp and is generated by the database server.

Required conceptual type:

```text
DateTime(timezone=True)
NOT NULL
server_default = now()
```

Application clients must not supply or override the authoritative audit timestamp.

This provides one server-controlled timeline for actions performed by multiple users and system actors.

Separate `created_at`/`updated_at` fields are not required for an immutable audit record.

---

## 15. Transactional Integrity

Business mutation, `AuditOperation` creation and all associated `AuditRecord` inserts must participate in the same transaction.

Required invariant:

```text
COMMIT:
    business change ✓
    audit operation ✓
    audit record(s) ✓

ROLLBACK:
    business change ✗
    audit operation ✗
    audit record(s) ✗
```

Audit must not use a separate database session or independent transaction.

The generic `UnitOfWork` contract must remain audit-agnostic. Audit repositories must use the same transaction/session boundary established by the application infrastructure.

### Current verification gap

The current code confirms the existence of the `UnitOfWork` abstraction and its commit/rollback boundary, but the exact SQLAlchemy session wiring has not yet been conclusively identified from the current Infrastructure/dependency implementation.

Therefore the following statement is a **required target invariant**, not a claim that the current implementation already satisfies it:

> Audit persistence and the business mutation must use the same concrete SQLAlchemy transaction.

---

## 16. Separation of Concerns

Audit Trail is not a replacement for business history.

The responsibilities are separate:

```text
Business entity/history
    ↓
current and domain-specific state

Audit Trail
    ↓
who / initiated by / when / what / why / operation
```

Domain Events also remain a separate concern:

```text
Domain Event
    ↓
notify / coordinate application behavior

Audit Trail
    ↓
mandatory persistent historical trace
```

The existence of a Domain Event does not by itself satisfy the audit requirement.

---

## 17. Architectural Boundaries

The Audit implementation must follow the project Constitution:

```text
API
  ↓
Application
  ↓
Domain / shared contracts
  ↑
Infrastructure
  ↓
Database
```

The following are prohibited:

- FastAPI dependencies inside Audit domain logic;
- SQLAlchemy models inside Domain;
- direct database access from API routers;
- audit logic implemented as legacy CRUD;
- mandatory audit persistence only in a post-commit event handler;
- audit-specific knowledge embedded in the generic `UnitOfWork` contract.

The Application layer owns the use-case transaction boundary. Infrastructure owns persistence implementation.

---

## 18. Security and Integrity Requirements

The audit mechanism must preserve historical accountability even when a user is later archived or deactivated.

`actor_id` and `initiated_by` therefore reference stable User identity and must remain meaningful after the actor can no longer authenticate.

The audit journal itself must not become mutable merely because the referenced user is archived.

Authorization remains a separate concern. Existing business authorization determines whether a user may perform the operation; Audit Trail records which authenticated user actually performed it.

System/background actors must also be identifiable. Anonymous audit operations are prohibited.

---

## 19. Current State vs Required State

### Already available in current code

- authenticated `User` identity;
- Application-level authenticated-user propagation for protected mutations;
- Application authorization for Verification approve/reject;
- `UnitOfWork` abstraction with commit/rollback behavior;
- Domain Events infrastructure;
- logical `archived` state on the shared model base.

### Not yet implemented

- persistent `AuditOperation` model;
- persistent `AuditRecord` model;
- Audit Repository contract;
- Infrastructure audit persistence;
- transactional audit write integration;
- immutable database/application enforcement for audit records;
- operation correlation generation/propagation;
- field-level change generation;
- audit read/query contract;
- complete system-wide audit-worthy operation matrix;
- concrete system/background actor representation;
- retention/indexing/migration implementation.

---

## 20. Open Design Questions

The following remain deliberately open until the relevant current code is audited:

1. Exact Audit domain/shared contract and ownership.
2. Exact SQLAlchemy persistence model and migration.
3. How field-level changes are generated without duplicating business logic.
4. How `operation_id` is propagated through nested application operations.
5. Exact concrete transaction/session wiring needed to guarantee that Audit and business mutation share one SQLAlchemy transaction.
6. Exact representation and lifecycle of the system/background actor.
7. Which additional modules and use cases are mandatory in the first audit rollout.
8. Whether audit read access requires a dedicated read model and authorization policy.
9. Retention and operational storage requirements for long-term history.
10. Whether multi-record correction relationships are required beyond the current Verification scope.

These questions must be answered from the current code and explicit business requirements before implementation.

---

## 21. Decision Summary

Approved decisions:

```text
1. Audit Trail is required system-wide for significant business changes.
2. Audit must identify the direct actor by stable User.id or an identifiable system actor.
3. A logical operation has an initiator separate from the direct actor when necessary.
4. Audit and business mutation must be atomic in the same transaction.
5. Current post-commit Domain Events are not the mandatory audit mechanism.
6. Audit uses field-level changes as the primary change representation.
7. changes is persisted as JSONB.
8. entity_type is a stable application-level string.
9. action is a stable application-level string using <entity_type>.<operation>.
10. occurred_at is authoritative database-server time.
11. AuditOperation.operation_id and AuditRecord.id are UUIDs generated at the Application boundary.
12. Audit is append-only; historical records are never silently deleted, updated or archived.
13. Invalid/unreliable audit information is documented by a new corrective/invalidation record linked to the original record.
14. Verification history is never physically deleted.
15. Invalid/unreliable Verification data is archived/invalidated with reason and history, and corrections are separate records.
16. reason is nullable in the common audit contract and is required by concrete use cases where business rules demand it.
17. Verification reject/archive/correct operations require reason; approve does not.
18. operation_id correlates all audit records belonging to one logical operation.
19. Audit remains separate from Domain Event notification and business entity state.
20. The exact concrete SQLAlchemy transaction/session wiring remains an implementation verification task.
```

Implementation must begin only after the remaining open design questions are resolved from the actual project contracts.