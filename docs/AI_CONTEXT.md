# Sfera Project AI Context

## Назначение проекта

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

## Архитектура

Проект использует:

```text
DDD + Clean Architecture
```

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

Domain не зависит от ORM, SQLAlchemy, Infrastructure и API.

Application использует Repository Interfaces и Unit of Work.

Infrastructure содержит SQLAlchemy repositories, ORM mapping и database access.

API содержит FastAPI routers, schemas и DI. Business logic в API отсутствует.

## Backend Status

DDD/Clean Architecture migration:

```text
COMPLETE
```

Legacy CRUD:

```text
REMOVED
```

Validation:

```text
pytest -q
33 passed

ruff check .
All checks passed

ruff format --check .
352 files already formatted
```

Current branch:

```text
develop
```

Latest synchronized commit:

```text
6386c5b feat: configure frontend api and cors
```

## Deployment Checkpoint — 2026-08-17

Backend runs as:

```text
sfera-backend.service
active (running)
```

Startup:

```text
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Verified:

```text
GET /health -> {"status":"ok"}
GET /orders/ -> []
```

Added:

- ORM model registry import on startup;
- CORSMiddleware for frontend.

## Frontend Current Checkpoint

Frontend stack:

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

Feature architecture is used.

Implemented orders flow:

- orders list;
- order details;
- create order;
- update order;
- register order action;
- query cache update after mutation.

API integration:

```text
VITE_API_URL
 ↓
axios http.ts
 ↓
FastAPI backend
```

Runtime:

```text
Frontend Vite: 0.0.0.0:5173
Backend: 0.0.0.0:8000
```

Remote access:

```text
http://top.vlsfera.ru:5173
ZeroTier: 10.147.17.242
```

Frontend configuration:

- `src/shared/api/http.ts` uses `import.meta.env.VITE_API_URL`;
- `vite.config.ts` allows external host `top.vlsfera.ru`;
- backend CORS allows frontend origin.

Validation:

```text
npm run typecheck
passed

npm run build
passed
```

## Next Development Direction

Frontend development continues incrementally:

```text
Frontend Architecture
 ↓
Application Shell
 ↓
Backend API Integration
 ↓
One User Scenario
 ↓
Validate
 ↓
Next Scenario
```

Next tasks:

1. Define frontend production deployment model.
2. Add customer selection flow for order creation.
3. Add authentication foundation.
4. Continue user scenarios.

Documentation:

- `docs/AI_CONTEXT.md`
- `docs/MIGRATION_STATUS.md`
- `docs/ARCHITECTURE.md`
- `docs/FRONTEND_ARCHITECTURE.md`
