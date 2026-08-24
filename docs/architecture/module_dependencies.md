# Зависимости модулей

Версия: 1.1

---

# Общая схема

```text
                FastAPI
                   │
                   ▼
              API (Routers)
                   │
                   ▼
             Application
              (Services)
                   │
                   ▼
                Domain
         (Entities, Events)
                   │
                   ▼
            Repository Port
                   │
                   ▼
          Infrastructure
      (SQLAlchemy Repository)
                   │
                   ▼
              PostgreSQL
```

---

# Правило зависимостей

Зависимости направлены только вниз.

```
API
 ↓

Application
 ↓

Domain
 ↓

Infrastructure
 ↓

Database
```

Обратные зависимости запрещены.

---

# API

Каталог

```
app/api/
```

Отвечает за:

- HTTP;
- маршруты;
- валидацию входных данных;
- вызов сервисов.

Не содержит бизнес-логики.

---

# Application

Каталог

```
app/application/
```

Содержит:

- сервисы;
- use cases;
- Unit of Work.

Отвечает за выполнение сценариев работы.

---

# Domain

Каталог

```
app/domains/
```

Содержит:

- сущности;
- Value Objects;
- события;
- фабрики;
- интерфейсы репозиториев.

Не зависит от SQLAlchemy и FastAPI.

---

# Infrastructure

Каталог

```
app/infrastructure/
```

Содержит:

- реализации Repository;
- SQLAlchemy;
- интеграции;
- внешние сервисы.

Реализует интерфейсы Domain.

---

# Models

Каталог

```
app/models/
```

ORM-модели SQLAlchemy.

Используются только Infrastructure и Alembic.

---

# CRUD

Каталог

```
app/crud/
```

Назначение:

простые операции доступа к данным.

Не содержит бизнес-логики.

---

# Schemas

Каталог

```
app/schemas/
```

Содержит Pydantic-модели:

- Create;
- Update;
- Read.

---

# Shared

Каталог

```
app/shared/
```

Общие компоненты проекта:

- Aggregate;
- DomainEvent;
- EventDispatcher;
- Repository;
- Value Objects.

---

# Database

Каталог

```
app/db/
```

Содержит:

- подключение;
- Session;
- Base;
- настройки SQLAlchemy.

---

# Alembic

Каталог

```
alembic/
```

Используется исключительно для миграций.

---

# Направление вызовов

```
HTTP Request

↓

Router

↓

Service

↓

Repository Interface

↓

SQLAlchemy Repository

↓

PostgreSQL
```

---

# Domain Events

```
Entity

↓

Domain Event

↓

EventDispatcher

↓

Handler
```

---

# Unit of Work

```
Router

↓

Service

↓

UnitOfWork

↓

Repository

↓

Commit
```

---

# Запрещённые зависимости

Нельзя:

```
Domain
    ↓
FastAPI
```

```
Domain
    ↓
SQLAlchemy ORM
```

```
Models
    ↓
Services
```

```
Router
    ↓
Database
```

```
Schemas
    ↓
Repository
```

---

# Разрешённые зависимости

```
Router
    ↓
Service
```

```
Service
    ↓
Repository
```

```
Repository
    ↓
Models
```

```
Models
    ↓
BaseModel
```

---

# Основной принцип

Каждый слой знает только о нижележащем слое.

Ни один внутренний слой не зависит от внешнего.
