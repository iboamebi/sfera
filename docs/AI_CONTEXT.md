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

Authorization migration для concrete business use cases с определённым владельцем операции завершена.

Последующий backend этап добавил корректное восстановление `Order.items` из persistence и публичный read contract `OrderRead.items`.

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

## Order Items Checkpoint

Завершён incremental Orders stage по отображению позиций заказа.

Backend:

```text
OrderModel.order_items
        ↓
OrderMapper.to_domain()
        ↓
Domain Order.items
        ↓
OrderRead.items
```

Изменения покрыты infrastructure mapper test и полным backend suite.

Frontend:

```text
OrderApiDto.items
        ↓
orderMapper
        ↓
OrderRead.items
        ↓
OrderItems
        ↓
OrderDetails
```

Frontend DTO и model разделены; `instrument_id` преобразуется в `instrumentId`.

`OrderItems` является отдельным UI-компонентом и не содержит business logic.

## Latest Validation

Backend:

```text
pytest -q
134 passed
```

Последняя точечная infrastructure validation:

```text
1 passed
ruff check — All checks passed!
ruff format --check — 1 file already formatted
```

Frontend:

```text
npm run typecheck — passed
npm run build — passed
```

Vite сообщил только стандартное предупреждение о bundle chunk > 500 kB; текущий build завершился успешно.

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
- order items display;
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

Authorization migration завершена для всех текущих use cases с определённым business owner.

Orders order-items stage завершён: persistence mapping, backend read contract и frontend display реализованы и валидированы.

Следующий independent feature stage выбирается после аудита актуального `develop`; не продолжать authorization механически и не следовать устаревшему roadmap без проверки фактического кода.

Для `Device`, `InstrumentType`, `PriceList`, `Workflow` не вводить authorization без нового explicit business requirement.

## Recovery Checkpoint

При продолжении после паузы:

1. прочитать `docs/AI_WORKING_PROTOCOL.md`;
2. прочитать `docs/AI_CONTEXT.md`;
3. прочитать нормативные и соответствующие security/architecture документы;
4. проверить актуальный `develop` и последние commits;
5. определить следующий independent use case по фактическому состоянию кода.
