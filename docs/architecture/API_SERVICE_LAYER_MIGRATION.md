# API Service Layer Migration

## Версия

v1.0

## Дата

2026-07-19

---

# Назначение

Настоящий документ фиксирует завершение миграции REST API проекта «Сфера» с прямого использования CRUD на использование Application Service Layer.

Документ является контрольной точкой архитектуры проекта.

---

# Исходная архитектура

До выполнения рефакторинга взаимодействие выполнялось следующим образом:

```text
HTTP Request
      |
      v
FastAPI Router
      |
      v
CRUD
      |
      v
SQLAlchemy
      |
      v
PostgreSQL
```

### Недостатки

- API зависел от CRUD.
- CRUD содержал элементы прикладной логики.
- Сложно внедрять бизнес-правила.
- Невозможно централизованно использовать Unit of Work.
- Отсутствовал единый слой Application Services.

---

# Новая архитектура

После рефакторинга используется следующая схема:

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
Repository
      |
      v
CRUD
      |
      v
SQLAlchemy
      |
      v
PostgreSQL
```

---

# Основные изменения

## 1. BaseRouter

### Было

```python
BaseRouter(
    crud=customer_crud,
)
```

### Стало

```python
BaseRouter(
    service_factory=customer_service_factory,
)
```

Теперь Router не знает о CRUD.

---

## 2. Repository

Все Repository работают через BaseRepository.

### Было

```python
super().__init__(
    customer_crud,
    db,
)
```

### Стало

```python
super().__init__(
    db,
    customer_crud,
)
```

Во всех Repository используется единый порядок параметров.

---

## 3. BaseRepository

Repository стал единственной точкой доступа к CRUD.

Структура:

```text
Application Service
        |
        v
Repository
        |
        v
CRUD
```

---

## 4. Application Service

Добавлен промежуточный слой.

Теперь API взаимодействует только с сервисами.

```text
Router
    |
    v
Service
    |
    v
Repository
```

---

# Проверенные REST API

Проверка выполнена через Swagger.

Успешно протестированы:

```text
GET /customers/

GET /organizations/

GET /orders/

GET /order-items/

GET /verifications/

GET /diagnostics/

GET /repairs/

GET /materials/

GET /warehouses/

GET /warehouse-stocks/

GET /warehouse-movements/

GET /price-lists/

GET /price-list-items/
```

Результат:

```text
HTTP 200 OK
```

---

# Исправленные ошибки

В процессе миграции были обнаружены и устранены следующие проблемы.

## Repository constructor

Исправлен порядок параметров конструктора BaseRepository.

Во всех Repository выполнена унификация.

---

## ORM Relationships

Исправлены связи моделей:

- VerificationMethod ↔ Methodology
- Document ↔ Order

Добавлены:

- ForeignKey
- relationship()
- back_populates

---

## SQLAlchemy Mapper

Исправлены ошибки:

- отсутствующие relationship;
- отсутствующие back_populates;
- несогласованные ForeignKey;
- ошибки конфигурации Mapper.

После исправлений ORM успешно инициализируется.

---

# Проверка ORM

Проверены:

- загрузка моделей;
- создание Session;
- получение данных;
- выполнение SELECT;
- инициализация Mapper.

Ошибок ORM не обнаружено.

---

# Проверенные модули

| Модуль | Статус |
|--------|--------|
| Organization | ✅ |
| Customer | ✅ |
| Order | ✅ |
| OrderItem | ✅ |
| Verification | ✅ |
| Diagnostic | ✅ |
| Repair | ✅ |
| Material | ✅ |
| Warehouse | ✅ |
| WarehouseStock | ✅ |
| WarehouseMovement | ✅ |
| PriceList | ✅ |
| PriceListItem | ✅ |

---

# Итоговая архитектура

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

        Repository Interface

                  │

                  ▼

 Infrastructure Repository

                  │

                  ▼

          SQLAlchemy CRUD

                  │

                  ▼

            PostgreSQL
```

---

# Достигнутые результаты

В результате рефакторинга:

- Router больше не зависит от CRUD.
- CRUD отвечает исключительно за работу с базой данных.
- Repository стал единым слоем доступа к данным.
- Подготовлена основа для внедрения Domain Services.
- Подготовлена инфраструктура для Unit of Work.
- Подготовлена инфраструктура для Domain Events.
- Архитектура приведена к требованиям DDD и Clean Architecture.

---

# Следующий этап

Следующим этапом выполняется разработка Application Service Layer.

Последовательность внедрения:

1. CustomerService
2. OrderService
3. OrderItemService
4. VerificationService
5. DiagnosticService
6. RepairService
7. WarehouseService
8. ArshinService

После завершения данного этапа вся прикладная логика проекта будет полностью сосредоточена в слое Application Services.
