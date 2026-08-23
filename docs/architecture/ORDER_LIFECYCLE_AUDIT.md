# Order Lifecycle Audit

## Date

2026-08-23

## Scope

Аудит фактического состояния Order lifecycle после завершения Verification frontend action slice.

Цель:

- определить текущие переходы Order;
- проверить связь Order → Workflow → Verification/Repair/Diagnostic;
- определить безопасную следующую архитектурную точку.

Изменения кода в рамках аудита не выполнялись.

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
- переводит заказ в `REGISTERED`.

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

Также поддерживается CANCELLED.

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
- прямой order_item_id в текущей модели не обнаружен.

## Domain Events State

Инфраструктура существует:

```text
DomainEvent
EventDispatcher
```

Но отсутствует полный DDD event lifecycle:

```text
Aggregate
   ↓
collect events
   ↓
UnitOfWork
   ↓
EventDispatcher
   ↓
Handlers
```

Сейчас найдено:

- базовый DomainEvent;
- EventDispatcher;
- OrderCreated event.

Не найдено:

- OrderRegistered event;
- event handlers;
- subscriptions;
- workflow bootstrap через события.

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

## Next Candidate

Следующий независимый backend этап:

```text
DDD events foundation
```

Порядок:

1. общий AggregateRoot/event collection;
2. накопление domain events в агрегатах;
3. интеграция UnitOfWork;
4. dispatch после commit;
5. только затем OrderRegistered → workflow handler.

## Constraints

Не делать:

- добавление статусов без бизнес use case;
- прямое связывание Order с Repair/Diagnostic/Verification;
- создание workflow в API слое;
- возврат к CRUD orchestration.
