# Sfera Migration Status

## Текущий этап

Backend DDD/Clean Architecture migration завершена.

Текущий этап — stabilization after authentication/authorization foundation and incremental business user scenarios.

---

## Backend Architecture

Статус:

```text
COMPLETE
```

Архитектура:

```text
API
→ Application Service
→ Domain
→ Repository Interface
↑
Infrastructure Repository
→ Database
```

Проверено:

- Domain isolation;
- Application isolation;
- API isolation;
- Repository boundaries;
- mapper consistency;
- removal of legacy CRUD dependencies.

---

## Authentication / Authorization Checkpoint

Authentication foundation is implemented with server-side sessions.

```text
Browser
  ↓
HttpOnly session cookie
  ↓
server-side auth_sessions
  ↓
SessionApplicationService
  ↓
SessionRepository
```

Implemented:

- User domain and repository;
- Argon2 password hashing adapter;
- authentication application service;
- session domain;
- session repository interface;
- session ORM model and mapper;
- session repository;
- auth_sessions migration;
- login / current-user / logout contracts;
- authentication API dependencies;
- CSRF protection for cookie-authenticated state changes;
- initial authorization roles;
- UserRole value object;
- role persistence and migration;
- Application authorization contract;
- order registration authorization;
- API mapping of authorization failures to HTTP 403.

Current authorization rule:

```text
Order registration
  OPERATOR → allowed
  ADMIN    → allowed
  other    → forbidden
```

Authorization is kept in Application. The API only supplies the authenticated user and maps application authorization errors to HTTP responses.

Roles and permissions are not implemented as frontend-only checks.

---

## Audit Trail Checkpoint

Audit Trail foundation and the first transactional integration slice are complete.

Implemented:

- AuditOperation and AuditRecord application contracts;
- audit repository contracts;
- SQLAlchemy audit repositories;
- audit database models;
- Alembic migrations;
- audit repository dependency injection;
- Verification approve/reject audit integration;
- shared SQLAlchemy session and transaction boundary;
- automated audit/verification tests.

Status:

```text
Audit foundation:              COMPLETE
Persistence:                   COMPLETE
Verification integration:      COMPLETE
System-wide audit coverage:    OPEN
Audit read/query:              OPEN
DB append-only enforcement:    OPEN
```

The Audit Trail is not yet considered system-wide complete. Remaining mutation points require an audit coverage review.

## Current Read Architecture Checkpoint

Completed read-side migrations:

```text
Order
  - OrderReadService
  - OrderReadRepository
  - OrderReadData
  - dedicated read contract

Warehouse Stock
  - WarehouseStockReadService
  - WarehouseStockReadRepository
  - WarehouseStockReadData
  - SQLAlchemy read projection
  - GET /warehouse-stocks/warehouse/{warehouse_id}
```
Frontend read integration:

- Orders
- Customer
- Organization
- Material
- Verification
- Diagnostic
- Repair
- PriceList
- InstrumentType
- Warehouse Stock

---

## Backend Validation

Latest validated checkpoint:

```text
pytest -q
111 passed

ruff check .
All checks passed

ruff format --check .
410 files already formatted
```

Current branch:

```text
develop
```

Current HEAD:

```text
4238a5d docs: update authorization documentation
```

Working tree was clean before documentation synchronization.

---

## Deployment Checkpoint — 2026-08-17

Backend запущен через systemd:

```text
service:
sfera-backend.service

status:
active (running)

command:
/home/alex/sfera/backend/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Проверено:

```text
GET /health
→ {"status":"ok"}

GET /orders/
→ []
```

Добавлено:

- ORM model registry import при старте приложения;
- CORSMiddleware для frontend.

---

# Frontend Phase

Статус:

```text
IN PROGRESS
```

Frontend stack:

- React;
- TypeScript;
- Vite;
- React Router;
- TanStack Query;
- Axios;
- Material UI;
- React Hook Form;
- Zod.

---

## Реализовано

Orders feature:

- orders list;
- order details;
- create order;
- update order;
- register order action;
- query cache update after mutation;
- authentication route guard;
- login route;
- login form and validation;
- current-user query;
- protected application routes.

API integration:

```text
VITE_API_URL
    ↓
axios http.ts
    ↓
FastAPI backend
```

---

## Frontend Production Runtime

Frontend production deployment использует статический Vite build, размещенный в nginx.

```text
Browser
    ↓
nginx
    ├── React SPA static files
    │
    └── /api/*
          ↓
        FastAPI
```

SPA routing выполняется через fallback на:

```text
/index.html
```

Vite development server на `5173` не является частью production runtime.

Production frontend:

```text
http://top.vlsfera.ru
```

Backend production service:

```text
sfera-backend.service
```

Frontend deployment выполняется вручную. Автоматический frontend deployment пока не настроен.

---

## Frontend Validation

Последняя известная validation:

```text
npm run typecheck
passed

npm run build
passed
```

---

## Следующие шаги

1. Выполнить аудит фактического состояния develop.
2. Выбрать следующий независимый бизнес-сценарий.
3. Реализовывать сценарий через существующие DDD/Clean Architecture boundaries.
4. Не добавлять CRUD механически.
5. Не расширять authorization без явного business owner.

---

## Documentation Governance

Основные документы:

- `docs/AI_CONTEXT.md`;
- `docs/MIGRATION_STATUS.md`;
- `docs/ARCHITECTURE.md`;
- `docs/architecture/AUTHORIZATION.md`;
- `docs/architecture/AUTHENTICATION.md`;
- `docs/architecture/PROJECT_CONSTITUTION.md`;
- `docs/architecture/MIGRATION_MATRIX.md`;
- `docs/FRONTEND_ARCHITECTURE.md`.

Документация должна соответствовать фактическому состоянию repository.

`PROJECT_CONSTITUTION.md` не изменяется при обычной синхронизации состояния.

Работа продолжается:

```text
analyze → implement → validate → synchronize → next
```

Feature migration и architectural cleanup не смешиваются.
