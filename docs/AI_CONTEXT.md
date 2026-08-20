# Sfera Project AI Context

## Назначение

Этот документ содержит изменяющееся техническое состояние проекта «Сфера», checkpoints и ближайшее направление работы.

Постоянные правила работы ИИ находятся в:

```text
docs/AI_WORKING_PROTOCOL.md
```

Нормативные архитектурные правила находятся в:

```text
docs/architecture/PROJECT_CONSTITUTION.md
```

## Проект

Сфера — информационная система сервисного центра и метрологической лаборатории.

Основные направления:

- учёт средств измерений;
- поверка;
- ремонт;
- диагностика;
- документы;
- склад;
- финансы;
- интеграция с ФГИС Аршин.

Репозиторий:

```text
git@github.com:iboamebi/sfera.git
```

Основная рабочая ветка:

```text
develop
```

Локальный root:

```text
~/sfera
```

## Архитектура

Проект использует:

```text
DDD + Clean Architecture
```

Основное направление зависимостей:

```text
API
  ↓
Application
  ↓
Domain
  ↓
Repository Interface
  ↑
Infrastructure Repository
  ↓
Database
```

Legacy CRUD migration завершена.

## Backend Current State

Backend migration to DDD/Clean Architecture:

```text
COMPLETE
```

Legacy CRUD:

```text
REMOVED
```

Последний GitHub checkpoint:

```text
c5be3494 docs: update authorization use-case scope
```

Последовательность последних authorization commits:

```text
c5be3494 docs: update authorization use-case scope
1522231f feat: pass authenticated user to repair use cases
3ecb39ea feat: authorize repair use cases
0702bdd7 feat: pass authenticated user to diagnostic use cases
38c48e45 feat: authorize diagnostic use cases
```

## Authorization Checkpoint

Authorization добавлена только для concrete business use cases, для которых определён владелец операции:

```text
Order
  → OPERATOR / ADMIN

Customer
  → OPERATOR / ADMIN

Organization
  → OPERATOR / ADMIN

Material
  → WAREHOUSE / ADMIN

Warehouse
  → WAREHOUSE / ADMIN

Verification
  → METROLOGIST / ADMIN

Diagnostic
  → TECHNICIAN / ADMIN

Repair
  → TECHNICIAN / ADMIN
```

Для state-changing API authenticated `User` передаётся из API boundary в Application service.

Application выполняет `require_role(...)` до изменения Domain state.

Application и API tests покрывают authorization boundary и forwarding authenticated user.

Не определено business authorization для:

```text
Device
InstrumentType
PriceList
Workflow
```

Для этих модулей authorization **не добавлять**, пока не появится конкретный business requirement. Не создавать broad CRUD permission model и не угадывать владельца операции.

Актуальный authorization contract:

```text
docs/architecture/AUTHORIZATION.md
```

## Latest Backend Validation

Подтверждённая локальная validation после authorization/doc updates:

```text
pytest -q
133 passed

ruff check .
All checks passed!

ruff format --check .
411 files already formatted
```

## Authentication State

Authentication использует server-side sessions.

Текущая модель:

```text
Browser
  ↓
HttpOnly session cookie
  ↓
server-side auth_sessions
  ↓
SessionRepository
  ↓
PostgreSQL
```

Authentication и authorization остаются отдельными concerns.

Authentication foundation включает:

- User domain и repository;
- Argon2 password hashing adapter;
- authentication application service;
- session domain;
- session repository interface;
- session ORM model и mapper;
- session repository;
- `auth_sessions` migration;
- authentication API dependency;
- CSRF protection for state-changing cookie-authenticated requests.

Authentication contract находится в:

```text
docs/architecture/AUTHENTICATION.md
```

## Session Persistence Checkpoint

Session persistence foundation реализована в:

```text
backend/app/models/auth_session.py
backend/app/infrastructure/mappers/auth_session_mapper.py
backend/app/infrastructure/auth/session_repository.py
backend/tests/infrastructure/mappers/test_auth_session_mapper.py
backend/tests/infrastructure/auth/test_session_repository.py
```

ORM model зарегистрирован через:

```text
backend/app/db/model_registry.py
```

Migration:

```text
backend/alembic/versions/8f4c2d1a9b30_add_auth_sessions.py
```

Revision:

```text
8f4c2d1a9b30
```

Down revision:

```text
9a1ddec34200
```

Table:

```text
auth_sessions
```

Основные поля:

- `id`;
- `session_id` UNIQUE;
- `user_id` FK → `users.id`;
- `expires_at`;
- `revoked`;
- `created_at` с DB default.

Indexes:

- `session_id`;
- `user_id`;
- `expires_at`.

## User Persistence

Таблица `users` уже существовала в исходной Alembic schema.

Не создавать duplicate users table или migration.

ORM:

```text
backend/app/models/user.py
```

Repository:

```text
backend/app/infrastructure/user/user_repository.py
```

Mapper:

```text
backend/app/infrastructure/mappers/user_mapper.py
```

## Frontend Current State

Frontend использует:

```text
React
TypeScript
Vite
React Router
TanStack Query
Axios
Material UI
React Hook Form
Zod
```

Feature-oriented architecture используется в `frontend/src/features/`.

Готовы основные Orders flows:

- orders list;
- order details;
- create order;
- update order;
- register order;
- cache update after registration;
- customer selection.

Authentication UI foundation также существует:

- login route;
- login form and validation;
- login mutation;
- current-user query;
- protected route guard.

Frontend API layer:

```text
frontend/src/shared/api/http.ts
```

Production frontend уже собирается и разворачивается вручную через nginx.

## Production Deployment State

Runtime topology:

```text
ZeroTier client
    ↓
DNS: top.vlsfera.ru
    ↓
10.147.17.242:80
    ↓
nginx
    ├── React SPA
    │     /var/www/sfera
    │
    └── /api/*
          ↓
        127.0.0.1:8000
          ↓
        sfera-backend.service
          ↓
        PostgreSQL
```

Required persistent services:

```text
nginx.service
sfera-backend.service
```

Frontend production build and deployment are complete.

## DNS / ZeroTier State

Deployment remains ZeroTier-only.

Network:

```text
Sfera
01dce6d7bcdf5646
```

Server:

```text
10.147.17.242/24
```

Established hostnames include:

```text
dev.vlsfera.ru
top.vlsfera.ru
api.vlsfera.ru
db.vlsfera.ru
storage.vlsfera.ru
zt.vlsfera.ru
git.vlsfera.ru
grafana.vlsfera.ru
prometheus.vlsfera.ru
u6c.vlsfera.ru
```

Do not rename established infrastructure hostnames without explicit need.

## Documentation State

Stable working rules:

```text
docs/AI_WORKING_PROTOCOL.md
```

Volatile project state:

```text
docs/AI_CONTEXT.md
```

Architecture governance:

```text
docs/architecture/PROJECT_CONSTITUTION.md
docs/ARCHITECTURE.md
docs/MIGRATION_STATUS.md
docs/architecture/MIGRATION_MATRIX.md
docs/architecture/AUTHENTICATION.md
docs/architecture/AUTHORIZATION.md
docs/FRONTEND_ARCHITECTURE.md
```

`PROJECT_CONSTITUTION.md` не изменяется как обычная документация.

## Current Next Direction

Текущий development direction — incremental authorization concrete business use cases.

Authorization migration для всех use cases с определённым business owner завершена на текущем checkpoint.

Следующий use case выбирается только после чтения фактического Application service, API router, tests и соответствующих security/architecture документов из GitHub.

Для `Device`, `InstrumentType`, `PriceList`, `Workflow` не вводить authorization без нового explicit business requirement.

Следующий independent feature stage определяется после этого checkpoint; не продолжать authorization механически.

## Recovery Checkpoint

При продолжении после паузы:

1. прочитать `docs/AI_WORKING_PROTOCOL.md`;
2. прочитать `docs/AI_CONTEXT.md`;
3. прочитать нормативные и соответствующие security/architecture документы;
4. проверить актуальный `develop` и последние commits;
5. определить следующий independent use case по фактическому состоянию кода.
