# Sfera Domain Map

## Назначение документа

Документ описывает карту доменных областей системы Сфера.

Цель:

- определить границы модулей;
- зафиксировать зависимости между контекстами;
- предотвратить смешивание бизнес-логики;
- использовать как основу для дальнейшей разработки.


# Архитектурный подход

Проект использует:

- Domain Driven Design;
- Clean Architecture;
- Application Service Pattern.


Основное правило зависимостей:

```

API

↓

Application

↓

Domain

↓

Infrastructure

```


Domain Context не зависит от:

- FastAPI;
- SQLAlchemy;
- PostgreSQL;
- внешних интеграций.


# Bounded Contexts


## Customer Context

Назначение:

Управление заказчиками.


Ответственность:

- организации;
- контактные лица;
- реквизиты;
- условия обслуживания;
- скидки клиента.


Основная сущность:

```

Customer

```


Связи:

```

Customer

```
|
v
```

Order

```


---

# Device Context

Назначение:

Управление средствами измерений.


Ответственность:

- регистрация приборов;
- типы средств измерений;
- заводские номера;
- характеристики;
- принадлежность владельцу.


Основные сущности:

```

Device

DeviceType

```


Связи:

```

Customer

```
|
```

Device

```
|
```

Order

```


---

# Order Context

Назначение:

Центральный бизнес-контекст системы.


Ответственность:

- регистрация заказа;
- жизненный цикл заказа;
- объединение работ;
- контроль выполнения.


Aggregate Root:

```

Order

```


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


Связи:


```

Customer
|
v
Order
|
+---- OrderItem
|
+---- Verification
|
+---- Repair
|
+---- Diagnostic

```


---

# Verification Context

Назначение:

Управление поверкой средств измерений.


Ответственность:

- проведение поверки;
- результаты;
- даты;
- методики;
- подготовка данных для Аршин.


Основная сущность:

```

Verification

```


Связи:


```

Order

|

Verification

|

Arshin Export

```


---

# Repair Context

Назначение:

Управление ремонтом оборудования.


Ответственность:

- диагностика;
- ремонтные работы;
- замена компонентов;
- результаты ремонта.


Основные сущности:


```

Repair

RepairOperation

```


Связь:


```

Order

|

Repair

```


---

# Workflow Context

Назначение:

Управление технологическими процессами.


Ответственность:

- этапы работ;
- переходы состояний;
- шаблоны процессов.


Основные сущности:


```

Workflow

WorkflowTemplate

WorkflowStep

```


Связь:


```

Order

|

Workflow

```


---

# PriceList Context

Назначение:

Управление стоимостью.


Ответственность:

- прайс-листы;
- услуги;
- материалы;
- расчёт стоимости.


Aggregate Root:

```

PriceList

```


Структура:


```

PriceList

|

+---- PriceListItem

+---- PriceListItem

```


Связи:


```

PriceList

```
 |
```

Application Service

```
 |
```

Order

```


---

# Arshin Integration Context

Назначение:

Интеграция с ФГИС Аршин.


Ответственность:

- получение данных;
- подготовка экспорта;
- контроль отправленных результатов.


Основные сущности:


```

ArshinExport

ArshinRecord

```


Правило:


Arshin является внешней системой.

Внутренняя БД Сфера является источником бизнес-истины.


---

# Context Map


Общая схема:


```

```
            Customer
               |
               |
               v
```

Device -------> Order <------ PriceList

```
               |
               |
    +----------+----------+

    |          |          |

    v          v          v
```

Verification   Repair   Diagnostic

```
               |

               v

           Workflow


               |

               v

       Arshin Integration
```

```


# Application Layer Integration


Каждый контекст имеет собственный Application Service.


Пример:


```

CustomerApplicationService

DeviceApplicationService

OrderApplicationService

VerificationApplicationService

WorkflowApplicationService

PriceListApplicationService

```


# Repository Boundaries


Каждый домен имеет собственный Repository Interface:


```

CustomerRepository

DeviceRepository

OrderRepository

VerificationRepository

WorkflowRepository

PriceListRepository

```


Реализация:


```

Infrastructure Layer

```


# Development Rules


При добавлении нового модуля:


1. определить bounded context;

2. описать Aggregate Root;

3. создать Domain Entity;

4. определить Repository Interface;

5. реализовать Application Service;

6. добавить API;

7. покрыть тестами.


# Current Architecture Status


Sfera v2.0 Architecture:


```

✓ Customer

✓ Device

✓ Order

✓ Verification

✓ Workflow

✓ PriceList (design stage)

```


Документ является базовой картой доменной архитектуры проекта.
```
