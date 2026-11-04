# Customer Application Design

## Назначение

Customer — заказчик/контактная сущность сервисного центра. Клиент может существовать без юридического лица и может быть связан с несколькими Organization.

Документ описывает текущую целевую модель Customer в архитектуре DDD + Clean Architecture. Он заменяет ранний проектный эскиз CustomerService, в котором ошибочно предполагались обязательная Organization и legacy CRUD.

## Бизнес-сценарии

1. Создать Customer без Organization.
2. Создать Customer с одной или несколькими заранее заведёнными Organization.
3. Просмотреть Customer и связанные Organization.
4. Добавить или убрать связь с Organization, не создавая нового Customer.
5. Изменить контактные данные Customer.
6. Архивировать Customer без физического удаления.
7. Использовать Customer при создании Order независимо от наличия Organization.

Organization хранит юридические реквизиты. Выбор Organization-плательщика происходит при выставлении Invoice, не при создании Customer или Order.

## Архитектура

```text
Customer Router
      ↓
Customer Application Service
      ↓
Customer Domain
      ↓
Customer Repository Interface
      ↑
Customer SQLAlchemy Repository
      ↓
PostgreSQL
```

Application Service может использовать Organization Repository Interface для проверки существования организаций. SQLAlchemy и ORM остаются только в Infrastructure.

Legacy CRUD и старые CustomerService abstractions не возвращаются.

## Domain contract

Customer:
- `id`;
- `name`;
- `contact_person?`;
- `phone?`;
- `email?`;
- `comment?`;
- `discount_percent`;
- `organization_ids: list[UUID]`;
- `archived`.

`organization_ids` отражает связи через `customer_organizations`, а не старую колонку `customers.organization_id`.

## Application commands

### CreateCustomerCommand

- `name`;
- `organization_ids` — optional, default empty;
- contact fields;
- `discount_percent`.

### UpdateCustomerCommand

- `customer_id`;
- optional changed customer fields;
- `organization_ids` — optional; если передано, заменяет набор связей целиком.

Перед сохранением Application проверяет, что все переданные Organization существуют. Повторяющиеся идентификаторы не должны создавать дубли связей.

### DeleteCustomerCommand

Архивирует Customer. Физическое удаление запрещено.

## Persistence

- `customer_organizations` — фактическая таблица связей Customer ↔ Organization.
- Старые `customers.organization_id` и `orders.organization_id` остаются только как nullable legacy persistence fields на переходном этапе.
- Customer Repository читает и сохраняет association rows.
- Существующие связи, ранее перенесённые миграцией в `customer_organizations`, сохраняются.

## API contract

Customer response возвращает список связанных Organization identifiers. Управление набором связей выполняется через Customer create/update use cases; API не обращается к Repository или ORM напрямую.

## UI behavior

- При нуле организаций Customer создаётся без выбора Organization.
- При одной организации интерфейс может показать её как единственную связанную.
- При нескольких организациях пользователь выбирает нужные из списка.
- Создание Organization из формы Customer остаётся доступным, но не обязательным.
- Карточка Customer показывает связанные Organization.

## Validation

Покрываются:
- создание без Organization;
- создание с несколькими Organization;
- проверка существования каждой Organization;
- обновление списка связей;
- отсутствие дубликатов;
- чтение и сохранение связей Infrastructure;
- API contract;
- отсутствие Organization у нового Order;
- сохранение исторических legacy organization identifiers.

Этот модуль считается полностью перенесённым только после реализации и проверки бизнес-сценариев, а не только наличия Domain/Application/Repository/API слоёв.
