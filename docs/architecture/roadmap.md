# Sfera Development Roadmap

## Назначение документа

Документ описывает этапы развития системы Сфера.

Цель:

- определить порядок разработки;
- сохранить архитектурную последовательность;
- контролировать переходы между версиями;
- фиксировать завершённые этапы.


# Архитектурная версия

Текущая версия:

```

Sfera v2.0 Architecture

```

Baseline:

```

v2.0-architecture

```

Commit:

```

85cbf2a

```

Дата фиксации:

```

2026-07-27

```


# Phase 0 — Project Foundation

Статус:

```

COMPLETED

```


Выполнено:

- создание backend проекта;
- настройка Python окружения;
- настройка PostgreSQL;
- настройка Alembic;
- базовая структура приложения.


Результат:

```

Development Environment Ready

```


---

# Phase 1 — Domain Foundation

Статус:

```

COMPLETED

```


Выполнено:

- Domain primitives;
- Aggregate Root;
- Entity;
- Value Objects;
- Repository abstraction;
- Domain events.


Создано:

```

app/shared/domain
app/domains

```


Результат:

```

DDD Foundation

```


---

# Phase 2 — Core Business Domains

Статус:

```

COMPLETED

```


Реализовано:


## Device

Статус:

```

COMPLETED

```


Возможности:

- доменная модель прибора;
- repository;
- application layer;
- API.


---

## Order

Статус:

```

COMPLETED

```


Возможности:

- Order Aggregate;
- Order Items;
- жизненный цикл заказа;
- repository;
- application service;
- API.


---

## Verification

Статус:

```

COMPLETED

```


Возможности:

- поверка СИ;
- результаты;
- интеграция с заказом;
- application service.


---

# Phase 3 — Application Service Migration

Статус:

```

COMPLETED

```


Выполнено:

- перенос бизнес-операций из API;
- внедрение Application Service;
- Dependency Injection;
- разделение слоёв.


Модули:

```

Customer

Device

Order

Verification

Workflow

```


Результат:

```

Clean Architecture Migration Complete

```


---

# Phase 4 — Workflow Engine

Статус:

```

COMPLETED

```


Реализовано:

- workflow domain;
- workflow templates;
- workflow steps;
- application service;
- API.


Назначение:

управление технологическими процессами выполнения заказов.


---

# Phase 5 — Price Management

Статус:

```

IN PROGRESS

```


Модуль:

```

PriceList

```


Цель:

создание единой системы управления стоимостью.


План:


## Domain

```

PriceList

PriceListItem

```


## Application

```

PriceListApplicationService

```


## Infrastructure

```

SQLAlchemy Repository
Mapper
Models

```


## API

```

PriceList Router

```


## Tests

```

Domain tests

Application tests

API tests

```


---

# Phase 6 — Warehouse

Статус:

```

PLANNED

```


Цель:

управление материалами и комплектующими.


Функции:

- складские остатки;
- движения;
- резервирование;
- списание;
- закупки.


---

# Phase 7 — Finance

Статус:

```

PLANNED

```


Функции:

- расчёт стоимости;
- счета;
- оплаты;
- скидки;
- договорные цены.


---

# Phase 8 — Arshin Integration

Статус:

```

PLANNED

```


Функции:

- экспорт XLSM;
- проверка данных;
- история отправок;
- контроль статусов.


Правила:


Экспортируются только:

```

COMPLETED Verification

```

Не экспортируются:

```

Do not export flag
Invalid records

```


---

# Phase 9 — Documents

Статус:

```

PLANNED

```


Функции:

- шаблоны документов;
- акты;
- свидетельства;
- коммерческие предложения.


---

# Development Order

Каждый новый модуль реализуется:


```

1. Domain Design

2. Domain Entities

3. Repository Interface

4. Infrastructure Adapter

5. Application Service

6. API

7. Tests

8. Documentation

```


# Current Status


```

Foundation              ✓

DDD Architecture        ✓

Device                  ✓

Order                   ✓

Verification            ✓

Customer Migration      ✓

Workflow                ✓

PriceList               IN PROGRESS

Warehouse               NEXT

Finance                 PLANNED

Arshin                  PLANNED

Documents               PLANNED

```


# Version Strategy


```

v2.0
|
+-- Architecture baseline
|
+-- Application services
|
+-- Core domains

v2.1
|
+-- PriceList
+-- Warehouse

v2.2
|
+-- Finance
+-- Documents

v3.0
|
+-- Full production release

```


# Rules

Новые изменения должны:

- сохранять DDD структуру;
- не переносить бизнес-логику в API;
- использовать Application Service;
- использовать Repository Pattern;
- сопровождаться документацией.
```
