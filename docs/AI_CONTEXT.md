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

Domain не зависит от ORM, SQLAlchemy, Infrastructure и API.

Application использует Repository Interfaces и Unit of Work.

Infrastructure содержит SQLAlchemy repositories, ORM mapping и database access.

API содержит FastAPI routers, schemas и DI. Business logic в API отсутствует.

Legacy CRUD migration завершена. Feature migration и архитектурный cleanup не смешиваются.

## Backend Status

DDD/Clean Architecture migration:

```text
COMPLETE
```

Legacy CRUD:

```text
REMOVED
```

Последние backend validation results:

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

Документация синхронизирована с текущим состоянием проекта отдельными commits в `develop`.

## Backend Deployment Checkpoint — 2026-08-17

Backend запускается через systemd:

```text
sfera-backend.service
```

Service state:

```text
enabled
active
```

Startup command:

```text
/home/alex/sfera/backend/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Verified locally through nginx:

```text
GET /api/health -> {"status":"ok"}
GET /api/orders/ -> []
```

Backend additions already integrated:

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

Feature-oriented architecture is used.

Implemented Orders flow:

- orders list;
- order details;
- create order;
- update order;
- register order action;
- query cache update after mutation.

Frontend API layer:

```text
src/shared/api/http.ts
```

It creates the Axios client and uses:

```text
import.meta.env.VITE_API_URL
```

API feature modules use this shared HTTP client.

Backend DTOs are separated from frontend models where transport naming/details should not leak into UI code.

## Frontend Production Deployment — COMPLETE

The frontend no longer requires a Vite development server for normal runtime.

Production model:

```text
Browser
  ↓
http://top.vlsfera.ru
  ↓
nginx :80
  ├── /      → /var/www/sfera
  └── /api/  → 127.0.0.1:8000
```

Vite production build:

```text
npm run typecheck
PASS

npm run build
PASS
```

Build output is deployed to:

```text
/var/www/sfera
```

Static files are owned by `root:root` with directories `755` and files `644`.

Frontend deployment is currently manual. No automatic deployment pipeline is part of the current runtime model.

nginx configuration:

```text
/etc/nginx/sites-available/sfera
/etc/nginx/sites-enabled/sfera
```

The default nginx site was removed from `sites-enabled`.

nginx service state:

```text
enabled
active
```

Configuration validation:

```text
sudo nginx -t
→ successful
```

Current nginx virtual host:

```text
server_name top.vlsfera.ru;
root /var/www/sfera;
```

SPA routing:

```text
location / {
    try_files $uri $uri/ /index.html;
}
```

API reverse proxy:

```text
location /api/ {
    proxy_pass http://127.0.0.1:8000/;
}
```

Production verification from the server:

```text
GET http://127.0.0.1/ with Host: top.vlsfera.ru
→ 200 OK

GET http://127.0.0.1/api/health with Host: top.vlsfera.ru
→ {"status":"ok"}

GET http://127.0.0.1/api/orders/ with Host: top.vlsfera.ru
→ []
```

Production verification from another ZeroTier node:

```text
http://top.vlsfera.ru/
→ 200 OK

http://top.vlsfera.ru/api/health
→ {"status":"ok"}
```

No Vite dev server is required or expected on port `5173` in production.

## DNS / ZeroTier Deployment

The deployment is ZeroTier-only.

ZeroTier network:

```text
Sfera
01dce6d7bcdf5646
```

Server ZeroTier address:

```text
10.147.17.242/24
```

The server runs dnsmasq for the Sfera ZeroTier network.

Relevant configuration:

```text
/etc/dnsmasq.d/sfera.conf
```

Current host records include:

```text
dev.vlsfera.ru        → 10.147.17.2
top.vlsfera.ru        → 10.147.17.242
api.vlsfera.ru        → 10.147.17.242
db.vlsfera.ru         → 10.147.17.242
storage.vlsfera.ru   → 10.147.17.242
zt.vlsfera.ru        → 10.147.17.242
git.vlsfera.ru       → 10.147.17.242
grafana.vlsfera.ru   → 10.147.17.242
prometheus.vlsfera.ru → 10.147.17.242
u6c.vlsfera.ru       → 10.147.17.3
```

The public DNS zone does not currently resolve `top.vlsfera.ru`; this is intentional for the current ZeroTier-only deployment model.

Do not rename the established hostnames. They may be required for future infrastructure expansion.

Existing masquerading/NAT configuration predates this deployment and should not be recreated or changed without explicit need.

## Deployment Architecture

Current runtime topology:

```text
ZeroTier client
    ↓
DNS: top.vlsfera.ru
    ↓
10.147.17.242:80
    ↓
nginx
    ├── static React SPA
    │     /var/www/sfera
    │
    └── /api/*
          ↓
        127.0.0.1:8000
          ↓
        sfera-backend.service
          ↓
        FastAPI
          ↓
        PostgreSQL
```

Required persistent services:

```text
nginx.service
sfera-backend.service
```

Both services are enabled and active.

## Frontend Routing Note

React Router uses:

```text
/orders
/orders/new
/orders/:orderId
```

nginx must keep SPA fallback to `/index.html` so direct navigation and browser refreshes on frontend routes do not produce server-side 404 responses.

The previous `Unexpected Application Error! 404 Not Found` was caused by testing the production SPA before the nginx static root and SPA fallback were correctly deployed. The current nginx configuration serves `/orders` through the SPA fallback and has been verified with `curl`.

## Important Development Rules

Work incrementally:

```text
analyze → one file → y → next
```

Rules:

- do not change backend DDD/Clean Architecture without explicit task;
- do not reintroduce CRUD patterns;
- API contains no business logic;
- SQLAlchemy remains in Infrastructure;
- preserve Repository Interfaces and Unit of Work boundaries;
- do not mix feature migration with architectural cleanup;
- read current code before changing it;
- never assume a file, module or API exists;
- keep documentation synchronized with implementation.

For Python changes run:

```text
pytest -q
ruff check .
ruff format --check .
```

For frontend changes run:

```text
npm run typecheck
npm run build
```

After a completed code stage:

```text
git status
git add ...
git commit
git push origin develop
```

Verify GitHub synchronization before continuing to the next stage.

## Next Development Direction

Frontend production deployment is complete.

Continue frontend development incrementally:

```text
Production Runtime
 ↓
One User Scenario
 ↓
Validate
 ↓
Next Scenario
```

Recommended next feature sequence:

1. Customer selection flow for order creation.
2. Authentication foundation.
3. Continue order-centric user scenarios.
4. Add additional domain workflows incrementally.

## Documentation Governance

Authoritative architecture order is defined by `PROJECT_CONSTITUTION.md`.

Documentation set:

- `docs/architecture/PROJECT_CONSTITUTION.md` — normative architecture rules;
- `docs/ARCHITECTURE.md` — current architecture description;
- `docs/MIGRATION_STATUS.md` — current migration and deployment status;
- `docs/architecture/MIGRATION_MATRIX.md` — module migration matrix and architecture checkpoints;
- `docs/AI_CONTEXT.md` — AI recovery context;
- `docs/FRONTEND_ARCHITECTURE.md` — current frontend architecture.

`PROJECT_CONSTITUTION.md` is not modified during routine state synchronization because changing it requires a new approved constitution version.
