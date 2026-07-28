# Application Service Layer Development Plan

## Этап

Application Service Layer v1.0

## Назначение

Настоящий документ определяет план перевода бизнес-логики проекта «Сфера» из API и CRUD слоя в слой Application Services.

После завершения этапа вся прикладная логика будет сосредоточена в Application Layer, а API станет исключительно транспортным уровнем.

---

# Целевая архитектура

```text
API Router
    |
    v
Application Service
    |
    v
Domain
    |
    v
Repository Interface
    |
    v
Infrastructure Repository
    |
    v
SQLAlchemy
    |
    v
PostgreSQL
```

---

# Основные принципы

## API Layer

API отвечает только за:

- получение HTTP-запроса;
- валидацию входных данных;
- вызов Application Service;
- возврат HTTP-ответа.

API запрещается:

- обращаться к CRUD;
- использовать SQLAlchemy Session;
- выполнять бизнес-проверки;
- изменять состояние доменных объектов.

---

## Application Service

Application Service отвечает за:

- выполнение пользовательского сценария;
- бизнес-правила;
- координацию нескольких Repository;
- запуск Domain Events;
- управление транзакциями;
- вызов Unit of Work.

Именно здесь реализуется прикладная логика системы.

---

## Repository

Repository отвечает только за доступ к данным.

Repository запрещается:

- принимать бизнес-решения;
- изменять состояние доменных объектов;
- выполнять проверки бизнес-правил.

---

## CRUD

CRUD остается исключительно слоем работы с SQLAlchemy.

CRUD содержит:

- SELECT;
- INSERT;
- UPDATE;
- DELETE.

Никакой бизнес-логики в CRUD быть не должно.

---

# План миграции

## Этап 1. CustomerService

Статус:

```text
TODO
```

Функции:

- создание клиента;
- изменение клиента;
- архивирование;
- проверка дублирования;
- получение клиента;
- получение списка.

---

## Этап 2. OrderService

Статус:

```text
TODO
```

Функции:

- создание заказа;
- изменение статуса;
- закрытие заказа;
- контроль жизненного цикла.

Поддерживаемые статусы:

```text
NEW
REGISTERED
IN_WORK
WAITING
COMPLETED
ISSUED
CLOSED
```

---

## Этап 3. OrderItemService

Статус:

```text
TODO
```

Функции:

- добавление прибора в заказ;
- изменение параметров;
- назначение видов работ;
- контроль состава заказа.

---

## Этап 4. VerificationService

Статус:

```text
TODO
```

Функции:

- регистрация поверки;
- изменение результата;
- проверка корректности данных;
- подготовка экспорта Аршин.

Бизнес-правила:

- SUITABLE → обязательно заполнить valid_until;
- UNSUITABLE → обязательно заполнить unsuitable_reason;
- учитывать признак "не экспортировать в Аршин".

---

## Этап 5. DiagnosticService

Статус:

```text
TODO
```

Функции:

- создание диагностики;
- ведение версий;
- выбор текущей версии.

---

## Этап 6. RepairService

Статус:

```text
TODO
```

Функции:

- регистрация ремонта;
- списание материалов;
- завершение ремонта.

---

## Этап 7. WarehouseService

Статус:

```text
TODO
```

Функции:

- приход материалов;
- списание;
- перемещение;
- контроль остатков.

---

## Этап 8. ArshinService

Статус:

```text
TODO
```

Функции:

- подготовка XLSM;
- проверка данных;
- экспорт;
- отметка экспортированных результатов;
- журнал обмена.

---

# Общие компоненты

## Unit of Work

Все операции изменения данных выполняются через Unit of Work.

Назначение:

- единая транзакция;
- атомарность операций;
- откат изменений при ошибке.

---

## Domain Events

Используются события:

```text
CustomerCreated
CustomerUpdated
CustomerArchived

OrderCreated
OrderStatusChanged

VerificationCompleted
VerificationExported

RepairCompleted

WarehouseStockChanged
```

---

## Domain Exceptions

Создать каталог:

```text
app/domain/exceptions/
```

Минимальный набор исключений:

```text
CustomerNotFound
CustomerAlreadyExists

OrderNotFound
InvalidOrderStatus

VerificationExportError

RepairNotAllowed

InsufficientStock
```

---

# Порядок реализации

1. CustomerService
2. OrderService
3. OrderItemService
4. VerificationService
5. DiagnosticService
6. RepairService
7. WarehouseService
8. ArshinService

Каждый этап завершается:

- реализацией Service;
- обновлением Repository;
- модульными тестами;
- проверкой через Swagger;
- фиксацией отдельным Git Commit.

---

# Критерии завершения

Application Service Layer считается завершённым после выполнения следующих условий:

- ни один Router не обращается напрямую к CRUD;
- вся бизнес-логика находится в Application Service;
- Repository содержит только операции доступа к данным;
- CRUD выполняет только операции SQLAlchemy;
- все REST API проходят проверку;
- модульные тесты проходят успешно;
- архитектура соответствует DDD/Clean Architecture.

---

# Итоговая схема

```text
HTTP Request
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
Repository Interface
      |
      v
Infrastructure Repository
      |
      v
SQLAlchemy CRUD
      |
      v
PostgreSQL
```

После завершения данного этапа вся прикладная логика проекта «Сфера» будет сосредоточена в Application Layer, что обеспечит масштабируемость, тестируемость и соответствие принципам DDD и Clean Architecture.
