# Sfera Product Backlog

## Назначение документа

Документ содержит перечень функциональных и архитектурных задач проекта Сфера.

Используется для:

- планирования разработки;
- контроля прогресса;
- определения следующих этапов;
- сохранения архитектурной последовательности.


# Current Architecture Baseline

Версия:

```

Sfera v2.0 Architecture

```

Baseline:

```

v2.0-architecture

```

Основные принципы:

- DDD;
- Clean Architecture;
- Application Service Pattern;
- Repository Pattern;
- Domain Events.


# Completed Tasks


## Architecture Foundation

Статус:

```

DONE

```

Выполнено:

- базовая структура проекта;
- Domain Layer;
- Application Layer;
- Infrastructure Layer;
- API Layer;
- Repository abstraction.


---

## Shared Domain Kernel

Статус:

```

DONE

```

Реализовано:

- Aggregate Root;
- Entity;
- Value Object;
- Domain Events;
- Event Dispatcher.


---

## Device Module

Статус:

```

DONE

```

Реализовано:

- Device Domain;
- Device Repository;
- SQLAlchemy Adapter;
- Application Service;
- API.


---

## Order Module

Статус:

```

DONE

```

Реализовано:

- Order Aggregate;
- Order Items;
- Order workflow states;
- Repository;
- Application Service;
- API actions.


---

## Verification Module

Статус:

```

DONE

```

Реализовано:

- Verification Domain;
- результаты поверки;
- связь с Order;
- Application Service;
- API.


---

## Customer Module

Статус:

```

DONE

```

Реализовано:

- Customer Application Service;
- API migration;
- Repository integration.


---

## Workflow Module

Статус:

```

DONE

```

Реализовано:

- Workflow Domain;
- Workflow Template;
- Workflow Steps;
- Application Service;
- API.


---

# In Progress


# PriceList Module

Статус:

```

IN PROGRESS

```


Назначение:

Управление стоимостью услуг и материалов.


## Domain

Создать:

```

PriceList

PriceListItem

```


Задачи:

- определить Aggregate Root;
- реализовать бизнес-правила;
- добавить domain exceptions;
- добавить domain tests.


---

## Repository

Создать:

```

PriceListRepository

```


Методы:

```

get_by_id()

get_active()

save()

delete()

find_price()

```


---

## Infrastructure

Создать:

```

SQLAlchemyPriceListRepository

```


Задачи:

- модели БД;
- mapper;
- repository adapter.


---

## Application

Создать:

```

PriceListApplicationService

```


Commands:

```

CreatePriceList

UpdatePriceList

ActivatePriceList

AddPriceListItem

RemovePriceListItem

```


Queries:

```

GetPriceList

GetActivePriceList

GetPriceByServiceCode

```


---

## API

Создать:

```

price_list.py

```


Endpoints:

```

GET    /price-lists

POST   /price-lists

GET    /price-lists/{id}

PUT    /price-lists/{id}

POST   /price-lists/{id}/items

```


---

## Tests

Добавить:

```

domain tests

application tests

repository tests

api tests

```


# Next Modules


# Warehouse Module

Статус:

```

PLANNED

```


Функции:

- складские остатки;
- материалы;
- движения;
- резервирование;
- списание.


Основные сущности:

```

Warehouse

StockItem

Movement

```


---

# Finance Module

Статус:

```

PLANNED

```


Функции:

- расчёт стоимости;
- счета;
- платежи;
- скидки;
- договорные цены.


---

# Arshin Integration

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

Экспорт:

```

только COMPLETED Verification

```


Не экспортировать:

```

do_not_export = true

```


---

# Documents Module

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

# Technical Improvements


## Test Coverage

Статус:

```

PLANNED

```


Задачи:

- расширить domain tests;
- добавить integration tests;
- добавить API tests.


---

## CI/CD

Статус:

```

PARTIAL

```


Задачи:

- автоматический запуск тестов;
- проверка миграций;
- lint;
- quality checks.


---

## Documentation

Статус:

```

IN PROGRESS

```


Задачи:

- обновление архитектурных документов;
- описание новых bounded contexts;
- ADR для значимых решений.


# Development Sequence


Каждый новый модуль:


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


# Current Progress


```

Architecture             DONE

Domain Kernel             DONE

Device                    DONE

Order                     DONE

Verification              DONE

Customer                  DONE

Workflow                  DONE

PriceList                 IN PROGRESS

Warehouse                 PLANNED

Finance                   PLANNED

Arshin                    PLANNED

Documents                 PLANNED

```


# Backlog Rule

Любая новая функциональность должна:

- иметь описание доменной модели;
- иметь владельца бизнес-правила;
- сохранять границы контекстов;
- реализовываться через Application Service;
- сопровождаться тестами и документацией.
