# Sfera Migration Status

## Текущий этап

Backend DDD/Clean Architecture migration завершена.

Текущий этап — frontend development and production validation.

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

## Backend Validation

Последняя validation:

```text
pytest -q
33 passed

ruff check .
All checks passed

ruff format --check .
352 files already formatted
```

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
- query cache update after mutation.

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
https://top.vlsfera.ru
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

## Следующие frontend шаги

1. Добавить customer selection flow для создания заказа.
2. Проверить order creation через UI с реальным Customer UUID.
3. Добавить authentication foundation.
4. Определить и реализовать автоматизацию frontend production deployment.

---

## Documentation Governance

Основные документы:

- `docs/AI_CONTEXT.md`;
- `docs/MIGRATION_STATUS.md`;
- `docs/ARCHITECTURE.md`;
- `docs/architecture/PROJECT_CONSTITUTION.md`;
- `docs/architecture/MIGRATION_MATRIX.md`;
- `docs/FRONTEND_ARCHITECTURE.md`.

Документация должна соответствовать фактическому состоянию repository.

Работа продолжается:

```text
analyze → one file → y → next
```

Feature migration и architectural cleanup не смешиваются.
