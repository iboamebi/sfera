# Domain Layer

**Версия:** 1.1
**Дата актуализации:** 2026-07-16

---

# 1. Назначение

Domain Layer содержит бизнес-модель проекта «Сфера».

Это ядро системы, в котором находятся правила предметной области.

Domain не зависит от:

- FastAPI;
- SQLAlchemy;
- PostgreSQL;
- Alembic;
- внешних сервисов.

---

# 2. Роль Domain Layer

Domain отвечает за:

- бизнес-сущности;
- жизненные циклы объектов;
- ограничения;
- инварианты;
- доменные события;
- бизнес-правила.

---

# 3. Расположение

```text
app/domains/
```

---

# 4. Домены системы

Основные бизнес-домены:

```text
domains/

├── order
├── device
├── verification
├── repair
├── warehouse
└── shared
```

---

# 5. Структура домена

Пример:

```text
order/

├── entities/
├── value_objects/
├── events/
├── services/
├── repositories/
└── factories/
```

---

# 6. Entity

Entity — объект с уникальной идентичностью и жизненным циклом.

Основные сущности:

```text
Order

OrderItem

Device

Verification

Repair
```

---

# 7. Aggregate

Aggregate объединяет связанные сущности и контролирует изменение состояния.

Главный агрегат системы:

```text
Order
```

Через Order управляются связанные производственные процессы.

---

# 8. Order Aggregate

Структура:

```text
Order

├── OrderItem
│
├── Diagnostic
│
├── Repair
│
└── Verification
```

---

# 9. Value Objects

Value Object описывает объект без собственной идентичности.

Примеры:

```text
Money

VerificationResult

DateRange

Address
```

---

# 10. Domain Services

Используются для правил, которые не принадлежат одной сущности.

Примеры:

```text
VerificationDecisionService

PricingCalculationService
```

---

# 11. Repository Interfaces

Domain определяет интерфейсы доступа к данным.

Пример:

```text
OrderRepository

VerificationRepository

DeviceRepository
```

Реализация находится в Infrastructure.

---

# 12. Factories

Factory создаёт сложные объекты с соблюдением правил.

Примеры:

```text
OrderFactory

VerificationFactory
```

---

# 13. Domain Events

События описывают значимые изменения состояния.

Примеры:

```text
OrderRegistered

OrderCompleted

VerificationFinished

RepairCompleted

DeviceConnected
```

---

# 14. Инварианты

Инварианты должны выполняться всегда.

Примеры:

- Order должен иметь заказчика;
- OrderItem принадлежит только одному Order;
- Verification невозможна без OrderItem;
- завершённая поверка не изменяет результат;
- склад не допускает отрицательных остатков.

---

# 15. Жизненный цикл заказа

```text
NEW

↓

REGISTERED

↓

IN_WORK

↓

WAITING

↓

COMPLETED

↓

ISSUED

↓

CLOSED
```

---

# 16. Правила разработки Domain

Разрешено:

- чистый Python;
- бизнес-логика;
- внутренние зависимости.

Запрещено:

- SQL-запросы;
- HTTP;
- ORM;
- файловая система;
- внешние API.

---

# 17. Тестирование

Domain покрывается Unit-тестами.

Тесты должны проверять:

- правила;
- переходы состояний;
- ограничения;
- события.

База данных не используется.

---

# 18. Главный принцип

Domain является единственным источником бизнес-правил системы.

Все остальные слои существуют только для использования и поддержки доменной модели.
