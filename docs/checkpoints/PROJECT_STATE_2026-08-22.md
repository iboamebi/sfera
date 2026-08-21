# Project State Checkpoint — 2026-08-22

## Current repository state

Branch:

```text
develop
```

Latest commits relevant to the current work:

```text
480d4d4 test: cover instrument type transaction commits
838fd16 fix: inject unit of work into instrument type service
04d53d1 fix: commit instrument type mutations
e3ab9c8 fix: pass mutation context to instrument type callback
b8766d1 fix: preserve instrument type creation callback
```

## Backend validation

```text
135 passed
```

InstrumentType application regression:

```text
1 passed
```

Frontend validation:

```text
npm run typecheck — passed
npm run build — passed
```

Latest frontend build observed:

```text
1240 modules transformed
vite build — passed
```

Vite reports a chunk-size warning above 500 kB; build succeeds.

## Completed current scenario

The current order-item → Device flow was extended so that a user can create an InstrumentType from the Device form.

Verified:

- Device form accepts instrument number;
- InstrumentType creation request exists;
- InstrumentType creation returns HTTP 201;
- created InstrumentType contains `id` and `archived: false`;
- InstrumentType initially did not persist because the Application service did not commit its transaction;
- UnitOfWork was added to InstrumentTypeApplicationService;
- DI was updated to inject the UnitOfWork;
- application regression test was updated to verify commits;
- backend regression now passes with 135 tests;
- after the transaction fix, a newly created InstrumentType appears in `GET /instrument-types/`;
- the created InstrumentType now appears in the Device form selector.

## Current blocker

Creating a Device (СИ) from the form currently fails:

```text
POST /devices → HTTP 500
```

The exact backend exception/traceback has not yet been identified.

Do not change frontend or backend code based on speculation. First capture the actual backend traceback for the failing POST `/devices` request.

The current `DeviceApplicationService.create()` already uses a UnitOfWork and validates that the referenced InstrumentType exists before creating the Device.

## Tomorrow — task order

### 1. Diagnose Device creation 500

- reproduce `POST /devices`;
- capture the complete backend traceback;
- identify the exact failing layer: Application, Domain, Infrastructure, ORM mapping, transaction, or API schema;
- read the affected file and its direct dependencies;
- make the smallest architectural fix;
- add/update regression coverage at the appropriate layer;
- run the focused test;
- run the full backend suite.

### 2. Re-test Device creation end-to-end

Verify:

```text
Create InstrumentType
→ select InstrumentType
→ create Device
→ POST /devices → 201
→ Device exists in GET /devices
```

### 3. Complete the order-item scenario

After Device creation is fixed:

```text
create/select Device
→ create order item
→ position appears in Order details
→ position remains after reload
```

Do not move to unrelated frontend features until this user scenario is complete.

## Documentation rules

- `docs/architecture/PROJECT_CONSTITUTION.md` remains unchanged.
- `docs/AI_WORKING_PROTOCOL.md` remains stable; volatile state belongs in checkpoints/context.
- Security rules remain governed by `AUTHENTICATION.md` and `AUTHORIZATION.md`.
- No authorization is to be added to Device or InstrumentType without an explicit business requirement.
- Keep DDD + Clean Architecture boundaries intact.
- Work one file/small step at a time.
