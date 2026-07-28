# Sfera Architecture Documentation

## Назначение

Каталог содержит архитектурную документацию проекта Сфера.

Документация используется для:

- проектирования новых модулей;
- контроля архитектурных решений;
- поддержки разработки;
- сохранения истории изменений.


# Architecture Baseline

Текущая архитектурная версия:

```

Sfera v2.0 Architecture

```

Git tag:

```

v2.0-architecture

```

Основные принципы:

```

Domain Driven Design

Clean Architecture

Application Service Pattern

Repository Pattern

Domain Events

Dependency Injection

```


# Documentation Structure

```

docs/

├── adr/
│   └── Architecture Decision Records
│
├── architecture/
│   └── Общая архитектура проекта
│
├── domain/
│   └── Доменные модели
│
├── api/
│   └── API документация
│
└── engines/
└── Внутренние механизмы системы

```


# Architecture Layers


## API Layer

Назначение:

- HTTP интерфейс;
- валидация запросов;
- преобразование DTO;
- вызов Application Services.


Расположение:

```

backend/app/api/

```


---

## Application Layer

Назначение:

- выполнение бизнес-сценариев;
- координация действий;
- управление транзакционными операциями.


Расположение:

```

backend/app/application/

```


Примеры:


```

OrderApplicationService

CustomerApplicationService

VerificationApplicationService

WorkflowApplicationService

```


---

## Domain Layer

Назначение:

- бизнес-правила;
- агрегаты;
- сущности;
- доменные события.


Расположение:

```

backend/app/domains/

```


Основные контексты:


```

Customer

Device

Order

Verification

Workflow

PriceList

```


---

## Infrastructure Layer

Назначение:

- работа с БД;
- внешние сервисы;
- технические реализации.


Расположение:

```

backend/app/infrastructure/

```


Примеры:


```

SQLAlchemy repositories

Database adapters

External integrations

```


# Domain Contexts


## Customer

Ответственность:

- заказчики;
- организации;
- контактные данные.


## Device

Ответственность:

- средства измерений;
- типы приборов;
- характеристики.


## Order

Центральный бизнес-контекст.


Ответственность:

- регистрация заказа;
- жизненный цикл;
- управление работами.


Статусы:


```

NEW

REGISTERED

IN_WORK

WAITING

COMPLETED

ISSUED

CLOSED

```


## Verification

Ответственность:

- поверка СИ;
- результаты;
- подготовка данных Аршин.


## Workflow

Ответственность:

- технологические процессы;
- этапы выполнения;
- переходы состояний.


## PriceList

Ответственность:

- стоимость услуг;
- стоимость материалов;
- расчёт цены.


# Development Process


Новый модуль создаётся в следующем порядке:


```

1. Domain Design

2. Domain Entity

3. Domain Exceptions

4. Repository Interface

5. Infrastructure Adapter

6. Application Service

7. API Router

8. Tests

9. Documentation

```


# Architecture Rules


## Rule 1

Domain не зависит от внешних технологий.


Запрещено:


```

Domain

↓

FastAPI

↓

SQLAlchemy

```


---

## Rule 2

API не содержит бизнес-логику.


Правильно:


```

API

↓

Application Service

↓

Domain

```


---

## Rule 3

Repository Interface находится в Domain.


Реализация:

```

Infrastructure

```


---

## Rule 4

Каждый новый бизнес-контекст имеет собственную границу ответственности.


# Current Status


```

Architecture Foundation     ✓

DDD Kernel                  ✓

Device                      ✓

Order                       ✓

Verification                ✓

Customer                    ✓

Workflow                    ✓

PriceList                   IN PROGRESS

```


# Related Documents


## ADR

```

docs/adr/

```


## Domain Documentation

```

docs/domain/

```


## API Documentation

```

docs/api/

```


## Development Planning

```

backlog.md

roadmap.md

checklist.md

```


# Version History


## v2.0 Architecture


Включает:


```

✓ Domain Layer

✓ Application Services

✓ Repository Abstraction

✓ API Migration

✓ Workflow Module

✓ Documentation Baseline

```


# Future Architecture Work


Планируется:


```

Storage Service

Audit Logging

Arshin Integration

Document Engine

Warehouse Domain

Finance Domain

```


# Rule

Архитектурные изменения должны сопровождаться:

- ADR;
- обновлением документации;
- изменением roadmap;
- изменением backlog;
- проверкой тестов.
```
