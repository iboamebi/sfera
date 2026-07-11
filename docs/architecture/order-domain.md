# Order Domain

## Aggregate Root

Order

## Child Entities

- OrderItem

## Value Objects

- OrderNumber
- OrderStatus
- Priority
- Deadline

## Domain Events

- OrderCreated
- OrderRegistered
- OrderStarted
- OrderCompleted
- OrderIssued
- OrderClosed
- OrderCancelled

## Repository

OrderRepository

## Domain Services

OrderLifecycleService
OrderValidationService

## Factory

OrderFactory

## Policies

OrderCanStartPolicy
OrderCanClosePolicy
OrderCanCancelPolicy

## Invariants

- Заказ всегда имеет номер.
- Заказ всегда имеет заказчика.
- Заказ содержит минимум один OrderItem.
- Закрытый заказ нельзя изменить.
- Отмененный заказ нельзя восстановить.
- Завершить заказ можно только после завершения всех работ по OrderItem.
