# Infrastructure Layer Standard

## Версия

v1.0

## Назначение

Настоящий документ определяет единый стандарт реализации Infrastructure Layer проекта «Сфера».

Infrastructure Layer реализует все технические детали работы системы и является адаптером между Domain Layer и внешним миром.

---

# Место в архитектуре

```text
HTTP

 │

 ▼

FastAPI Router

 │

 ▼

Application Service

 │

 ▼

Domain

 │

 ▼

Repository Interface

 │

 ▼

==========================
   INFRASTRUCTURE LAYER
==========================

 │

 ▼

SQLAlchemy

 │

 ▼

PostgreSQL
```

---

# Назначение Infrastructure Layer

Infrastructure отвечает за:

- реализацию Repository;
- работу с SQLAlchemy;
- работу с PostgreSQL;
- файловое хранилище;
- внешние API;
- импорт и экспорт данных;
- Unit of Work;
- Event Dispatcher;
- интеграции.

---

# Infrastructure запрещено

Infrastructure не должна:

- принимать бизнес-решения;
- изменять бизнес-правила;
- хранить прикладную логику;
- изменять состояние Domain Entity без участия Application Service.

---

# Структура проекта

```text
app/

└── infrastructure/

    ├── customer/
    │   └── customer_repository.py
    │
    ├── order/
    │   └── order_repository.py
    │
    ├── repair/
    │   └── repair_repository.py
    │
    ├── verification/
    │   └── verification_repository.py
    │
    ├── warehouse/
    │   └── warehouse_repository.py
    │
    ├── events/
    │
    ├── storage/
    │
    ├── arshin/
    │
    ├── sqlalchemy_unit_of_work.py
    │
    └── base_repository.py
```

---

# Repository

Каждый Repository реализует интерфейс Domain.

Пример:

```text
Domain

↓

CustomerRepository (interface)

↓

Infrastructure

↓

CustomerRepository (implementation)
```

Repository содержит только доступ к данным.

---

# SQLAlchemy

Infrastructure полностью отвечает за ORM.

Разрешено использовать:

```text
Session

relationship()

mapped_column()

select()

joinedload()

ForeignKey()

Index()

Constraint()
```

Domain не должен знать об этих объектах.

---

# BaseRepository

Все Repository наследуются от BaseRepository.

Стандарт:

```python
class CustomerRepository(BaseRepository):

    def __init__(self, db):
        super().__init__(
            db,
            customer_crud,
        )
```

Порядок аргументов фиксирован.

---

# CRUD

CRUD располагается только в Infrastructure.

Назначение CRUD:

- SELECT;
- INSERT;
- UPDATE;
- DELETE.

CRUD не содержит бизнес-логики.

---

# Unit of Work

Infrastructure реализует Unit of Work.

Назначение:

- begin();
- commit();
- rollback();
- управление транзакцией.

Application Service использует Unit of Work, но не реализует его.

---

# Event Dispatcher

Infrastructure реализует публикацию Domain Events.

Например:

```text
CustomerCreated

↓

Dispatcher

↓

Handler

↓

Email

↓

AuditLog

↓

Notification
```

---

# Storage

Infrastructure отвечает за хранение файлов.

Например:

```text
Документы

PDF

XLSX

Фотографии

Скан-копии

Архивы
```

Файлы не должны храниться в PostgreSQL без отдельного решения.

---

# Интеграции

Infrastructure содержит адаптеры внешних систем.

Например:

```text
ФГИС Аршин

SMTP

Telegram

LDAP

REST API

S3

MinIO
```

---

# ORM Mapping

Все модели SQLAlchemy находятся только в Infrastructure.

Допускается использование:

```python
relationship()

mapped_column()

ForeignKey()

association_proxy()

joinedload()
```

---

# Конфигурация

Infrastructure содержит:

```text
Database

Logging

Alembic

Redis

Celery

RabbitMQ

SMTP

Storage
```

Конфигурация не должна использоваться в Domain.

---

# Тестирование

Infrastructure тестируется интеграционными тестами.

Проверяются:

- работа Repository;
- выполнение SQL;
- транзакции;
- Unit of Work;
- подключение к PostgreSQL;
- внешние интеграции.

---

# Контроль качества

Infrastructure соответствует архитектуре, если:

- реализует только технические детали;
- не содержит бизнес-логики;
- реализует интерфейсы Domain;
- использует SQLAlchemy;
- использует PostgreSQL;
- не зависит от FastAPI Router;
- не содержит HTTP-кода.

---

# Итоговый стандарт

Infrastructure Layer является техническим адаптером проекта.

Любые изменения базы данных, ORM, файлового хранения или внешних интеграций должны ограничиваться Infrastructure Layer и не затрагивать Domain Layer.

Это обеспечивает независимость предметной области от технической реализации и полностью соответствует принципам Clean Architecture и Domain-Driven Design.
