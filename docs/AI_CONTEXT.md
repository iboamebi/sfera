# Sfera Project AI Context

## Назначение проекта

Сфера — информационная система сервисного центра и метрологической лаборатории.

Основное направление:

- учёт средств измерений (СИ);
- поверка средств измерений;
- ремонт;
- диагностика;
- технологические процессы;
- документы;
- склад;
- финансы;
- интеграция с ФГИС Аршин.

Основная бизнес-ценность системы:

- управление жизненным циклом средств измерений;
- проведение поверок;
- фиксация результатов;
- подготовка документов;
- экспорт данных в ФГИС Аршин.

---

# Ключевой бизнес-процесс

```
Order
    ↓
Case
    ↓
Workflow
    ↓
Technological Card
    ↓
Verification / Repair / Diagnostic
```

### Реализованные доменные объекты

- Organization
- Customer
- Order
- Material
- Warehouse
- Workflow
- Verification
- Repair
- Diagnostic
- PriceList

### Планируемые доменные объекты

- Case
- Technological Card

Статус:

```
ACTIVE DEVELOPMENT
```

---

# Технологический стек

## Backend

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- Docker / Docker Compose

## Инструменты качества

- pytest
- ruff
- pre-commit

---

# Репозиторий

GitHub:

```
iboamebi/sfera
```

Основная рабочая ветка:

```
develop
```

---

# Структура проекта

Основной backend:

```
backend/app/
```

```
api/
application/
domains/
infrastructure/
models/
schemas/
shared/
```

### Назначение слоёв

| Слой | Назначение |
|------|------------|
| API | HTTP-интерфейс |
| Application | Use Cases |
| Domain | Бизнес-правила |
| Infrastructure | Persistence и внешние интеграции |
| Models | SQLAlchemy ORM |
| Schemas | Pydantic API |
| Shared | Общие компоненты |

---

# Архитектура

Проект использует:

```
DDD + Clean Architecture
```

Целевая структура:

```
API
    ↓
Application Service
    ↓
Domain Model
    ↓
Repository Interface
    ↑
Infrastructure Repository
    ↓
Database
```

---

# Архитектурные правила

## Domain

Domain содержит:

- Entities;
- Aggregate Roots;
- Value Objects;
- Domain Services;
- Domain Exceptions;
- Repository Interfaces.

Разрешено:

- бизнес-правила;
- изменение состояния сущностей;
- доменная валидация.

Запрещено:

- SQLAlchemy;
- ORM;
- Session;
- Infrastructure;
- API.

---

## Application

Application содержит:

- Use Cases;
- Application Services;
- Commands;
- Application Exceptions.

Application:

- управляет сценариями использования;
- использует Domain;
- работает только через Repository Interfaces.

Запрещено:

- SQLAlchemy;
- ORM;
- Session;
- Infrastructure Repository;
- API.

---

## Infrastructure

Infrastructure содержит:

- реализации Repository Interface;
- SQLAlchemy;
- ORM mapping;
- работу с базой данных;
- внешние интеграции.

Запрещено:

- зависимость от API;
- зависимость от Application.

---

## API

API содержит:

- FastAPI routers;
- Request/Response Schemas;
- Dependency Injection;
- обработку Application Exceptions.

API:

- принимает HTTP-запрос;
- формирует Command;
- вызывает Application Service;
- возвращает результат.

Запрещено:

- бизнес-логика;
- Repository-вызовы;
- SQLAlchemy;
- прямой доступ к БД.

---

# Repository Boundary

## Domain Repository

Расположение:

```
app/domains/*/repositories/
```

Назначение:

- интерфейсы хранения;
- абстракции доступа к данным.

Запрещено:

- SQLAlchemy;
- Session;
- ORM.

---

## Infrastructure Repository

Расположение:

```
app/infrastructure/*/
```

Назначение:

- реализация Repository Interface;
- работа с SQLAlchemy;
- преобразование ORM ↔ Domain через Mapper.

Infrastructure подключается только через Dependency Injection.

---

# Текущее состояние проекта

Полностью завершена миграция на DDD/Clean Architecture для модулей:

- Organization
- Customer
- Order
- Material
- Warehouse
- PriceList
- Workflow
- Verification
- Repair
- Diagnostic

Для Workflow завершены:

- Domain entities;
- Repository interfaces;
- SQLAlchemy repositories;
- WorkflowMapper;
- WorkflowStageMapper;
- WorkflowInstanceMapper;
- WorkflowApplicationService;
- команды Start / Move / Complete;
- Dependency Injection;
- API migration;
- unit и architecture tests.

Architecture Baseline

Status:
DDD + Clean Architecture migration completed.

Current state:
- Domain layer isolated.
- Application layer independent from ORM.
- API contains no business logic.
- Infrastructure uses dedicated mappers.
- Legacy CRUD removed.

Current development focus:
Business functionality only.
Architecture cleanup is considered complete.
---

# Технический долг

После завершения основных миграций запланирована архитектурная очистка:

- удалить `app/domains/workflow/services/workflow_service.py`, если он останется простой обёрткой над методами `WorkflowInstance`;
- удалить связанные неиспользуемые экспорты и импорты;
- выполнять подобные упрощения только после завершения функциональных миграций.
