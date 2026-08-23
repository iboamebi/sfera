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
    +-- created_at
    +-- started_at
    +-- completed_at
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

## Acceptance and OrderItem Model Decision

Проектная документация по приёмке СИ определяет `OrderItem` не как простую ссылку на карточку прибора, а как конкретное СИ в конкретном заказе.

Зафиксировано следующее разделение ответственности:

```text
Device
└── постоянная карточка / электронный паспорт СИ
    └── постепенно обогащается по мере работы с прибором

Order
└── заказ / заявка

OrderItem
└── конкретное СИ в конкретном заказе
    ├── приёмочные данные
    ├── заказанные услуги
    ├── приоритет / подразделение / ответственный / сроки
    ├── текущее производственное состояние
    └── ссылка на Device

WorkflowInstance[]
└── история выполнения Workflow над OrderItem
```

### Правила

1. `Device` не дублируется целиком в `OrderItem`.
2. `OrderItem` не является только ссылкой на `Device`.
3. Приёмка должна требовать только данные, необходимые для дальнейшей работы.
4. Дополнительные сведения о СИ могут заполняться постепенно после приёмки.
5. Неполная карточка СИ не должна автоматически блокировать допустимую производственную работу.
6. Один `OrderItem` может проходить разные Workflow.
7. Workflow может быть выбран повторно.
8. Следующий Workflow выбирается после завершения текущей операции; выбор может быть произвольным и не обязан отличаться от предыдущего.
9. `WorkflowInstance[]` является историей выполнения, а не дублированием текущего состояния.
10. Для Workflow/операций timestamps обязательны.
11. Текущее состояние СИ в рамках заказа должно быть доступно без необходимости трактовать всю историю как текущее состояние.
12. Состав `OrderItem`, заказанных услуг и текущего состояния должен определяться по фактической доменной модели проекта, а не по существующей ORM-структуре.

### Acceptance Scenarios

Приёмка должна поддерживать быстрый сценарий:

```text
Новая заявка
    ↓
Добавить прибор
    ↓
Поиск существующей карточки Device
    ├── найден → использовать
    └── не найден → создать минимальную карточку
    ↓
Выбрать услуги
    ↓
Сохранить OrderItem
```

Для массовой приёмки общие параметры могут наследоваться от выбранного шаблона/набора позиций, а индивидуальные данные СИ остаются на уровне конкретного `OrderItem`.

## Workflow Semantics

Workflow является не фиксированным маршрутом всего заказа, а конкретным процессом, который может выполняться над отдельным `OrderItem`.

После завершения текущего Workflow возможны варианты:

```text
текущий Workflow завершён
        │
        ├── выбрать Workflow A
        ├── выбрать Workflow B
        ├── повторить Workflow A
        └── завершить обработку СИ
```

Поэтому `WorkflowInstance` хранит факт конкретного прохода процесса, включая timestamps, а не весь будущий маршрут СИ.

Пример:

```text
OrderItem
  │
  ├── WorkflowInstance: Поверка
  │       created_at → started_at → completed_at
  │
  ├── WorkflowInstance: Ремонт
  │       created_at → started_at → completed_at
  │
  └── WorkflowInstance: Поверка
          created_at → started_at → completed_at
```

Повторное выполнение того же Workflow является допустимым и не должно переиспользовать предыдущий `WorkflowInstance`.

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

`OrderItem` должен стать центральной операционной единицей конкретного СИ в заказе, но его окончательный контракт ещё не считается утверждённым до аудита существующей модели заказанных услуг и фактических полей `Device`/связанных сущностей.

## Next Candidate

Следующий независимый backend этап:

```text
OrderItem acceptance model → service/workflow selection → current state
```

Перед реализацией необходимо подтвердить существующие domain/application contracts для:

- заказанных услуг;
- Verification;
- Repair;
- Diagnostic;
- Device и InstrumentType;
- текущего состояния `OrderItem`.

Только после этого можно определить окончательный состав `OrderItem` и механизм выбора следующего Workflow.

## Constraints

Не делать:

- добавление статусов без бизнес use case;
- прямое связывание Order с Repair/Diagnostic/Verification;
- создание workflow в API слое;
- возврат к CRUD orchestration;
- придумывание отсутствующих workflow contracts;
- полное дублирование `Device` в `OrderItem` без подтверждённого бизнес-требования;
- считать `WorkflowInstance[]` одновременно историей и текущим состоянием без явного current-state контракта.
