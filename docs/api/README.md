# REST API

Версия: 1.0

---

# Назначение

Документ описывает структуру REST API проекта «Сфера».

API реализовано на FastAPI и предоставляет доступ ко всем функциям системы через HTTP.

---

# Базовый URL

```
/api
```

Документация Swagger:

```
/docs
```

OpenAPI:

```
/openapi.json
```

---

# Общие правила

Все запросы используют формат:

```
application/json
```

Ответы также возвращаются в формате JSON.

---

# CRUD

Для большинства сущностей поддерживаются стандартные операции.

```
POST

GET

PUT

DELETE
```

---

# Основные группы API

## Организации

```
/organizations
```

---

## Заказчики

```
/customers
```

---

## Заказы

```
/orders
```

---

## Позиции заказа

```
/order-items
```

---

## Средства измерений

```
/instruments

/instrument-types

/instrument-labels
```

---

## Поверка

```
/verifications

/methodologies
```

---

## Диагностика

```
/diagnostics
```

---

## Ремонт

```
/repairs
```

---

## Склад

```
/warehouses

/materials

/warehouse-stocks

/warehouse-movements
```

---

## Производство

```
/production-movements
```

---

## Документы

```
/documents

/document-templates
```

---

## Прайсы

```
/price-lists

/price-list-items
```

---

## Пользователи

```
/users

/roles

/permissions
```

---

# Стандартные ответы

Успешное создание:

```
201 Created
```

Успешное получение:

```
200 OK
```

Удаление:

```
204 No Content
```

---

# Ошибки

```
400 Bad Request

401 Unauthorized

403 Forbidden

404 Not Found

409 Conflict

422 Validation Error

500 Internal Server Error
```

---

# Архитектура

Каждый Router содержит только обработку HTTP-запросов.

Бизнес-логика размещается в сервисах.

Работа с базой данных выполняется через репозитории.

Схема взаимодействия:

```text
HTTP Request
      │
      ▼
Router
      │
      ▼
Service
      │
      ▼
Repository
      │
      ▼
PostgreSQL
```

---

# Версионирование

В дальнейшем планируется поддержка:

```
/api/v1

/api/v2
```

---

# Аутентификация

Планируется использование:

```
JWT Bearer Token
```

с разграничением доступа на основе ролей и разрешений.

---

# Основной принцип

REST API предоставляет единую точку доступа ко всем возможностям системы и не содержит бизнес-логики — она реализуется исключительно на уровне сервисов.
