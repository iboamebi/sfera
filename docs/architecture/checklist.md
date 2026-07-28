# Sfera Architecture Checklist

## Назначение документа

Документ содержит контрольный список требований к разработке и изменению системы Сфера.

Используется для:

- проверки новых модулей;
- контроля архитектурного качества;
- подготовки релизов;
- сохранения принципов DDD/Clean Architecture.


# Architecture Baseline

Текущая версия:

```

Sfera v2.0 Architecture

```

Baseline:

```

v2.0-architecture

```

Основные принципы:

```

DDD

Clean Architecture

Application Service Pattern

Repository Pattern

Domain Events

```


# Project Structure

## Layers

Проверка:

```

✓ Domain Layer

✓ Application Layer

✓ Infrastructure Layer

✓ API Layer

✓ Tests

```

Правило зависимостей:

```

API
|
v
Application
|
v
Domain
|
v
Infrastructure

```


# Domain Layer Checklist


Для каждого нового bounded context:


## Domain Design

```

□ описан бизнес-контекст

□ определён Aggregate Root

□ определены Entities

□ определены Value Objects

□ описаны бизнес-правила

```


## Domain Implementation

```

□ Entity создана

□ Aggregate Root реализован

□ Domain Exceptions добавлены

□ Domain Events определены при необходимости

□ отсутствуют зависимости от инфраструктуры

```


# Repository Checklist


Для каждого агрегата:


```

□ создан Repository Interface

□ методы соответствуют бизнес-операциям

□ интерфейс находится в Domain

□ реализация находится в Infrastructure

```


Структура:


```

Domain

```
Repository Interface
```

Infrastructure

```
Repository Implementation
```

```


# Infrastructure Checklist


Проверка:


```

□ SQLAlchemy models созданы

□ Mapper создан

□ Repository Adapter реализован

□ миграции Alembic добавлены

□ структура БД соответствует Domain

```


# Application Layer Checklist


Каждый модуль должен иметь:


```

□ Application Service

□ Commands

□ Queries

□ Dependency Injection

□ обработку бизнес-сценариев

```


Правило:


API не содержит бизнес-логику.


Неправильно:

```

Router

```
|
+-- расчёт цены

+-- изменение статуса

+-- бизнес-правила
```

```


Правильно:

```

Router

```
|
```

Application Service

```
|
```

Domain

```


# API Checklist


Проверить:


```

□ Router создан

□ зависимости подключены через DI

□ DTO определены

□ ошибки обработаны

□ API соответствует Application Layer

```


# Database Checklist


Перед миграцией:


```

□ модель проверена

□ relationships проверены

□ indexes определены

□ constraints определены

□ migration создана

```


После миграции:


```

□ alembic upgrade выполнен

□ тестовая БД проверена

□ rollback проверен

```


# Testing Checklist


## Domain Tests

```

□ Entity creation

□ Business rules

□ Exceptions

□ Aggregate behavior

```


## Application Tests

```

□ Commands

□ Services

□ Repository mocks

□ Business scenarios

```


## API Tests

```

□ endpoints

□ validation

□ permissions

□ responses

```


# Documentation Checklist


Каждый новый модуль:


```

□ Domain documentation

□ Architecture update

□ Roadmap update

□ Backlog update

□ ADR при необходимости

```


# Current Modules Status


## Completed


```

✓ Shared Domain Kernel

✓ Device

✓ Order

✓ Verification

✓ Customer

✓ Workflow

```


## In Progress


```

→ PriceList

```


## Planned


```

Warehouse

Finance

Arshin Integration

Documents

```


# PriceList Module Checklist


## Domain

```

✓ Domain Design

□ Entity

□ Exceptions

□ Tests

```


## Repository

```

□ Interface

□ SQLAlchemy Adapter

□ Mapper

```


## Application

```

□ Service

□ Commands

□ Queries

```


## API

```

□ Router

□ DTO

□ Tests

```


# Release Checklist


Перед созданием версии:


```

□ все тесты проходят

□ миграции применены

□ документация обновлена

□ CHANGELOG обновлён

□ tag создан

□ GitHub состояние проверено

```


# Development Rule


Новый код принимается только если:


```

Domain First

Application Second

Infrastructure Third

API Last

```


Бизнес-логика не должна находиться:

```

FastAPI Router

SQLAlchemy Model

Migration File

```


# Current Status


```

Sfera v2.0 Architecture

Architecture        ✓

Documentation       ✓

Core Domains        ✓

Application Layer   ✓

Workflow            ✓

PriceList           IN PROGRESS
