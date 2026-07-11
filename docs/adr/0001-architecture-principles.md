# ADR-0001 Architecture Principles

## Status

Accepted

## Date

2026-07-11

---

# Context

Проект "Сфера" разрабатывается как долгоживущая платформа для сервисного центра и метрологической лаборатории.

---

# Decisions

## 1. Architecture

Domain Driven Design

Clean Architecture

SOLID

---

## 2. Dependency Rule

```
Presentation
    ↓
Application
    ↓
Domain
    ↓
Infrastructure
```

---

## 3. Domain First

Любая новая функциональность начинается с доменной модели.

---

## 4. Aggregate First

Изменения выполняются через Aggregate Root.

---

## 5. Repository Pattern

Домен зависит только от Repository.

SQLAlchemy относится к Infrastructure.

---

## 6. ORM

ORM-модели не содержат бизнес-логики.

---

## 7. Business Rules

Вся бизнес-логика находится внутри Domain.

---

## 8. Events

Любое значимое изменение публикует Domain Event.

---

## 9. Backward Compatibility

Работающий backend не ломается.

Миграция выполняется постепенно.

---

## 10. Git

develop — основная разработка

main — стабильная версия

feature/* — новые функции

hotfix/* — исправления

---

## Consequences

Архитектура развивается без переписывания существующего проекта.
