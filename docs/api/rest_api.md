# REST API проекта «Сфера»

**Версия:** 1.1
**Дата актуализации:** 2026-07-16

---

# 1. Назначение

Документ описывает правила построения REST API системы «Сфера».

API предоставляет доступ к функциям сервисного центра и метрологической лаборатории.

---

# 2. Технология

Используется:

```text
FastAPI
```

Документация:

```text
Swagger UI

/docs
```

---

# 3. Архитектурный принцип

API является транспортным слоем.

Поток выполнения:

```text
HTTP Request

↓

Router

↓

Application Service

↓

Domain

↓

Repository

↓

Database
```

---

# 4. Базовый URL

Планируемая структура:

```text
/api/v1/
```

---

# 5. Формат данных

Основной формат:

```text
JSON
```

Кодировка:

```text
UTF-8
```

---

# 6. HTTP методы

Используются:

| Метод | Назначение |
|---|---|
| GET | получение данных |
| POST | создание |
| PUT | полное изменение |
| PATCH | частичное изменение |
| DELETE | удаление/архивирование |

---

# 7. Ответы API

Успешные ответы:

```text
200 OK

201 Created

204 No Content
```

Ошибки:

```text
400 Bad Request

401 Unauthorized

403 Forbidden

404 Not Found

409 Conflict

500 Internal Server Error
```

---

# 8. Основные ресурсы

## Customers

```text
/customers
```

Операции:

```text
GET

POST

PUT

DELETE
```

---

## Orders

```text
/orders
```

Операции:

```text
Create Order

Get Orders

Change Status

Close Order
```

---

## Order Items

```text
/order-items
```

---

## Instruments

```text
/instruments
```

---

## Verification

```text
/verifications
```

Операции:

```text
Create

Complete

Export
```

---

## Diagnostic

```text
/diagnostics
```

---

## Repair

```text
/repairs
```

---

## Warehouse

```text
/warehouses

/materials

/warehouse-stock

/warehouse-movements
```

---

## Pricing

```text
/price-lists

/price-list-items
```

---

## Documents

```text
/documents
```

---

# 9. Пагинация

Для списков используется:

```json
{
  "page": 1,
  "size": 50
}
```

---

# 10. Фильтрация

Фильтры передаются через query параметры.

Пример:

```text
/orders?status=IN_WORK
```

---

# 11. Ошибки

Стандартный формат:

```json
{
  "detail": "Error description"
}
```

---

# 12. Валидация

Входные данные проверяются через:

```text
Pydantic Schemas
```

---

# 13. Безопасность

API использует:

- аутентификацию;
- роли;
- разрешения.

Проверка выполняется до выполнения операции.

---

# 14. Версионирование

Изменения API должны сохранять обратную совместимость.

При несовместимых изменениях создаётся новая версия:

```text
/api/v2/
```

---

# 15. Тестирование

API проверяется через:

- автоматические тесты;
- Swagger;
- интеграционные сценарии.

---

# 16. Главный принцип

REST API должен предоставлять стабильный интерфейс доступа к бизнес-возможностям системы, не раскрывая внутреннюю архитектуру приложения.
