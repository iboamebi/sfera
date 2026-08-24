# Application Layer

**Версия:** 1.1
**Дата актуализации:** 2026-07-16

---

# 1. Назначение

Application Layer реализует сценарии использования системы «Сфера».

Он связывает внешний интерфейс, доменную модель и инфраструктуру.

Application управляет процессом выполнения операций, но не содержит бизнес-правил.

---

# 2. Место в архитектуре

```text
API

↓

Application

↓

Domain

↓

Infrastructure
```

---

# 3. Ответственность Application

Application отвечает за:

- выполнение Use Cases;
- координацию доменных объектов;
- управление транзакциями;
- вызов репозиториев;
- обработку команд;
- обработку запросов;
- публикацию доменных событий.

---

# 4. Не отвечает за

Application не содержит:

- HTTP-логику;
- SQL-запросы;
- ORM-модели;
- правила предметной области.

---

# 5. Расположение

```text
app/application/
```

---

# 6. Структура

```text
application/

├── services/
├── commands/
├── queries/
├── dto/
└── handlers/
```

---

# 7. Application Services

Service реализует законченный сценарий пользователя.

Примеры:

```text
OrderService

VerificationService

RepairService

WarehouseService

PricingService
```

---

# 8. Commands

Command изменяет состояние системы.

Примеры:

```text
CreateOrder

RegisterOrder

StartVerification

CompleteRepair

CloseOrder
```

---

# 9. Queries

Query только получает данные.

Примеры:

```text
GetOrder

GetVerificationHistory

GetWarehouseStock
```

---

# 10. DTO

DTO используются для передачи данных между слоями.

Правила:

- не содержат бизнес-логики;
- не являются ORM-моделями;
- используются для входных и выходных данных.

---

# 11. Работа с репозиториями

Application работает только через интерфейсы Domain.

Пример:

```text
OrderService

↓

OrderRepository

↓

SQLAlchemyOrderRepository
```

---

# 12. Unit Of Work

Application определяет границы транзакций.

Пример:

```text
Begin Transaction

↓

Load Aggregate

↓

Execute Operation

↓

Save Changes

↓

Commit
```

При ошибке:

```text
Rollback
```

---

# 13. Доменные события

После успешного изменения состояния Application публикует события.

Пример:

```text
OrderRegistered

VerificationFinished

RepairCompleted
```

---

# 14. Правила разработки

Разрешено:

- координация объектов;
- вызов сервисов;
- управление транзакциями.

Запрещено:

- SQL;
- HTTP;
- прямой доступ к ORM;
- размещение бизнес-правил.

---

# 15. Тестирование

Application покрывается:

- Unit-тестами сервисов;
- Integration-тестами с репозиториями.

Проверяются:

- сценарии использования;
- корректность транзакций;
- обработка ошибок.

---

# 16. Главный принцип

Application является координатором системы.

Он управляет выполнением процессов, сохраняя независимость Domain от технологий.
