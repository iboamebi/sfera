# Sfera API Layer

## Назначение

API Layer предоставляет внешний интерфейс системы Сфера.

Основные задачи:

- обработка HTTP запросов;
- валидация входных данных;
- преобразование DTO;
- вызов Application Services;
- возврат результатов.


API слой не содержит бизнес-логику.


# Architecture


Структура:


```

Client

|

v

FastAPI Router

|

v

Application Service

|

v

Domain

|

v

Infrastructure

```id="6f4q0k"


# API Responsibilities


API отвечает за:


```

✓ HTTP endpoints

✓ request validation

✓ response serialization

✓ authentication

✓ authorization

✓ dependency injection

```id="8w7v9j"


API не отвечает за:


```

✗ бизнес-правила

✗ изменение состояния агрегатов

✗ расчёт стоимости

✗ работу с базой напрямую

```id="m4e1fs"


# Router Structure


Расположение:


```

backend/app/api/routers/

```id="9p2fkp"


Текущие роутеры:


```

customer.py

device.py

order.py

verification.py

workflow.py

price_list.py

```id="5v7x8n"


# Dependency Injection


Зависимости подключаются через DI.


Пример:


```

Router

```
|
```

Depends()

```
|
```

Application Service

```
|
```

Repository

```id="9m3p4x"


API не создаёт:

```

SQLAlchemy Session

Repository

Domain Entity

```id="r1h4f2"


# DTO Layer


Для обмена данными используются DTO.


Структура:


```

Request DTO

```
 |
```

Application Service

```
 |
```

Response DTO

```id="j2l0s9"


DTO отвечает за:

- формат данных;
- валидацию;
- сериализацию.


DTO не содержит бизнес-правил.


# Current API Modules


## Customer API


Назначение:

- управление заказчиками;
- организации;
- контактные данные.


Application Service:


```

CustomerApplicationService

```id="4s3d8w"


---

## Device API


Назначение:

- средства измерений;
- типы устройств.


Application Service:


```

DeviceApplicationService

```id="g9k4b2"


---

## Order API


Назначение:

- создание заказов;
- управление состояниями;
- работа с позициями заказа.


Application Service:


```

OrderApplicationService

```id="h8k5p1"


---

## Verification API


Назначение:

- управление поверками;
- результаты;
- статусы.


Application Service:


```

VerificationApplicationService

```id="x3q7v5"


---

## Workflow API


Назначение:

- технологические процессы;
- этапы выполнения.


Application Service:


```

WorkflowApplicationService

```id="f5w8d0"


---

## PriceList API


Статус:

```

IN DEVELOPMENT

```id="z7r4s6"


Назначение:

- управление прайс-листами;
- управление ценами;
- расчёт стоимости.


Application Service:


```

PriceListApplicationService

```id="q8n2m4"


# Endpoint Rules


Каждый endpoint должен:


```

1. принять запрос

2. проверить DTO

3. вызвать Application Service

4. вернуть DTO ответа

```id="e2k5s8"


Пример потока:


```

POST /orders

Request DTO

```
|
```

OrderRouter

```
|
```

OrderApplicationService

```
|
```

Order Aggregate

```
|
```

Repository

```
|
```

Response DTO

```id="p4m7q1"


# Error Handling


Ошибки разделяются:


## Domain Errors


Примеры:


```

InvalidOrderStatus

PriceListNotActive

InvalidPrice

```id="u6s8z2"


Преобразуются API уровнем в HTTP ответы.


## Infrastructure Errors


Примеры:


```

DatabaseConnectionError

RepositoryError

```id="v3c9x5"


# Security


API должен поддерживать:


```

Authentication

Authorization

Role Based Access Control

Audit Logging

```id="k1d6m8"


# Testing


API тесты проверяют:


```

✓ endpoint availability

✓ validation

✓ authorization

✓ response format

✓ service invocation

```id="q7x4m2"


# API Development Rules


Новые endpoints создаются:


```

Domain

↓

Application Service

↓

API Router

```id="b5n8c3"


Запрещено:


```

Router

↓

Database

↓

Business Logic

```id="p9r2v7"


# Current Status


```

Customer API          ✓

Device API            ✓

Order API             ✓

Verification API      ✓

Workflow API           ✓

PriceList API          IN PROGRESS

```id="n4s7k9"


# Version


Architecture:

```

Sfera v2.0 Architecture

```id="d8m3q6"
```
