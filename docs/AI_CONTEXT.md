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

Последний известный GitHub checkpoint:

```text
50fd7ff feat: authorize customer deletion
```

Последовательность последних authorization commits:

```text
50fd7ff feat: authorize customer deletion
001deb1 feat: authorize customer updates
f8951c6 feat: pass authenticated user to customer creation
961f632 test: cover customer creation authorization
782aefd feat: authorize customer creation
140afec docs: define order update authorization
f0b3406 feat: authorize order updates
ee007d0 feat: authorize order item addition
```

Последний подтверждённый локальный backend validation:

```text
pytest -q
120 passed

ruff check .
All checks passed

ruff format --check .
410 files already formatted
```

## Customer Authorization Checkpoint

Customer soft delete уже существует:

- `Customer.archive()` используется вместо physical delete;
- default repository reads исключают archived customers;
- `include_archived=True` используется для специальных reads;
- DELETE API сохранён для backward compatibility.

Authorization последовательно добавлена для customer state-changing use cases:

```text
create
  ↓
operator/admin

update
  ↓
operator/admin

delete/archive
  ↓
operator/admin
```

Authenticated `User` передаётся из API boundary в Application service.

Application выполняет `require_role(...)` до изменения Domain state.

Application tests покрывают authorized/unauthorized behavior.

API tests покрывают authentication/CSRF dependencies и forwarding authenticated user в Application.

Authorization contract и актуальная матрица находятся в:

```text
docs/architecture/AUTHORIZATION.md
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

Последовательность уже начата с Order и Customer.

Следующий use case выбирается только после чтения фактического Application service, API router и соответствующих tests из GitHub.

Перед следующим feature stage необходимо учитывать текущие authorization contracts и не создавать broad CRUD permission model без явного business requirement.

## Recovery Checkpoint

При продолжении после паузы:

1. прочитать `docs/AI_WORKING_PROTOCOL.md`;
2. прочитать `docs/AI_CONTEXT.md`;
3. прочитать нормативные и соответствующие security/architecture документы;
4. проверить актуальный `develop` и последние commits;
5. определить следующий independent use case по фактическому состоянию кода.
