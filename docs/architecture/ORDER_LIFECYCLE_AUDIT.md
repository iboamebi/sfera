# Order Lifecycle Audit

## Date

2026-08-23

## Scope

Актуализация фактического состояния Order lifecycle после завершения Domain Events foundation.

Цель:

- определить текущие переходы Order;
- проверить связь Order → Workflow → Verification/Repair/Diagnostic;
- зафиксировать состояние domain events;
- определить следующую безопасную архитектурную точку.

## Current Order Lifecycle

Фактически реализовано:

```text
NEW
 |
v
REGISTERED
```

Поддержанные Order use cases:

- create;
- get;
- list;
- add_item;
- update;
- register.

`register()`:

- требует наличие хотя бы одной позиции;
- переводит заказ в `REGISTERED`;
- создаёт `OrderRegistered` domain event.

Следующие переходы статусов пока не реализованы:

```text
REGISTERED → IN_WORK
IN_WORK → WAITING
WAITING → COMPLETED
COMPLETED → ISSUED
ISSUED → CLOSED
```

## Domain Findings

### Order

Order является владельцем заказа.

OrderItem содержит:

- instrument_id;
- comment.

OrderItem не содержит:

- workflow_instance_id;
- verification_id;
- repair_id;
- diagnostic_id.

### Workflow

Workflow domain существует:

```text
Workflow
    |
    +-- WorkflowStage[]

WorkflowInstance
    |
    +-- workflow_id
    +-- order_item_id
    +-- current_stage
    +-- status
```

Workflow lifecycle:

```text
CREATED
  ↓
IN_PROGRESS
  ↓
COMPLETED
```

Также поддерживается `CANCELLED`.

## Process Domains

Обнаружена единая точка связи через OrderItem:

```text
OrderItem
    |
    +-- Repair
    |
    +-- Diagnostic
    |
    +-- WorkflowInstance
```

Repair:

```text
NEW
 ↓
IN_WORK
 ↓
WAITING
 ↓
COMPLETED
```

Diagnostic:

- создаётся через order_item_id;
- имеет собственный lifecycle.

Verification:

- отдельный aggregate;
- содержит результат поверки;
- approve/reject реализованы;
- прямой `order_item_id` в текущей модели не обнаружен.

## Domain Events State

Domain event foundation реализован:

```text
Aggregate
   ↓
collect events
   ↓
UnitOfWork
   ↓
commit
   ↓
EventDispatcher
   ↓
Handlers
```

Текущее состояние:

- `DomainEvent` — реализован;
- `AggregateRoot` — реализован;
- `OrderRegistered` — реализован;
- `EventDispatcher` — реализован;
- UnitOfWork event collection — реализован;
- dispatch после успешного commit — реализован;
- `OrderRegistered` handler — пока отсутствует;
- workflow bootstrap через события — пока отсутствует.

## Architectural Conclusion

Не рекомендуется реализовывать lifecycle как набор методов Order:

```python
order.start_work()
order.complete()
```

Текущая архитектура указывает на orchestration через процессы:

```text
Order
 |
 OrderItem
 |
 +-- WorkflowInstance
 +-- Repair
 +-- Diagnostic
```

Domain events теперь являются готовым механизмом для последующей orchestration.

## Next Candidate

Следующий независимый backend этап:

```text
OrderRegistered → workflow bootstrap
```

Перед реализацией handler необходимо подтвердить существующий application/infrastructure API для создания `WorkflowInstance` и определить, какой workflow должен запускаться для зарегистрированной позиции заказа.

## Constraints

Не делать:

- добавление статусов без бизнес use case;
- прямое связывание Order с Repair/Diagnostic/Verification;
- создание workflow в API слое;
- возврат к CRUD orchestration;
- придумывание отсутствующих workflow contracts.
