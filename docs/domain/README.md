# Sfera Domain Documentation

## Назначение

Каталог содержит документацию доменной модели системы Сфера.

Документы описывают:

- бизнес-области;
- сущности;
- агрегаты;
- правила предметной области;
- связи между контекстами.


# Domain Approach

Проект использует:

```

Domain Driven Design

```

Основная цель:

создать модель системы, отражающую реальные бизнес-процессы сервисного центра и метрологической лаборатории.


# Domain Layer Principles


## Business First

Доменная модель является источником бизнес-правил.


Логика должна находиться:


```

Domain Layer

```


а не:


```

API

Database Model

External Service

```


---

## Independence

Domain Layer не зависит от:


```

FastAPI

SQLAlchemy

PostgreSQL

External APIs

```


Domain должен быть тестируемым без инфраструктуры.


---

## Aggregate Based Design

Бизнес-операции выполняются через Aggregate Root.


Пример:


```

Order Aggregate

Order

|

+---- OrderItem

|

+---- Verification

|

+---- Repair

```


# Domain Contexts


## Customer


Назначение:

управление заказчиками.


Основные объекты:


```

Customer

Organization

```


Ответственность:


- данные клиентов;
- реквизиты;
- контакты;
- условия обслуживания.


---

## Device


Назначение:

управление средствами измерений.


Основные объекты:


```

Device

DeviceType

```


Ответственность:


- регистрация СИ;
- характеристики;
- принадлежность;
- состояние.


---

## Order


Центральный доменный контекст.


Основной агрегат:


```

Order

```


Ответственность:


- регистрация заказа;
- объединение работ;
- управление жизненным циклом.


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


---

## Verification


Назначение:

поверка средств измерений.


Основные объекты:


```

Verification

```


Ответственность:


- проведение поверки;
- результаты;
- даты;
- методики;
- данные для Аршин.


---

## Repair


Назначение:

ремонт средств измерений.


Ответственность:


- диагностика;
- ремонтные операции;
- замена компонентов;
- результаты.


---

## Workflow


Назначение:

управление технологическими процессами.


Основные объекты:


```

Workflow

WorkflowTemplate

WorkflowStep

```


Ответственность:


- этапы выполнения;
- переходы состояний;
- шаблоны работ.


---

## PriceList


Назначение:

управление стоимостью услуг и материалов.


Основной агрегат:


```

PriceList

```


Состав:


```

PriceList

|

+---- PriceListItem

```


Ответственность:


- хранение цен;
- расчёт стоимости;
- поддержка разных типов услуг.


---

# Domain Object Types


## Entity


Объект с уникальным идентификатором.


Примеры:


```

Order

Device

Customer

PriceList

```


---

## Value Object


Объект без собственной идентичности.


Примеры:


```

Money

Address

SerialNumber

MeasurementValue

```


---

## Aggregate Root


Главный объект агрегата.


Правила:


- контролирует изменения;
- защищает инварианты;
- является точкой входа.


Примеры:


```

Order

Device

PriceList

```


---

# Domain Events


Для значимых изменений используются события.


Примеры:


```

OrderCreated

VerificationCompleted

PriceListActivated

DeviceRegistered

```


События передаются через:


```

Domain Event Dispatcher

```


# Repository Interfaces


Каждый агрегат имеет собственный интерфейс хранения.


Примеры:


```

CustomerRepository

DeviceRepository

OrderRepository

VerificationRepository

WorkflowRepository

PriceListRepository

```


Реализация находится в:


```

Infrastructure Layer

```


# Domain Development Rules


Новый модуль создаётся:


```

1. Domain Design

2. Aggregate Root

3. Entities

4. Value Objects

5. Business Rules

6. Repository Interface

7. Application Service

8. Infrastructure Adapter

9. API

10. Tests

```


# Current Domain Status


Реализовано:


```

✓ Customer

✓ Device

✓ Order

✓ Verification

✓ Workflow

```


В разработке:


```

→ PriceList

```


Запланировано:


```

Warehouse

Finance

Documents

Arshin Integration

```


# Related Documentation


Архитектура:


```

docs/architecture/

```


ADR:


```

docs/adr/

```


API:


```

docs/api/

```


# Version


Current baseline:


```

Sfera v2.0 Architecture

```
```
