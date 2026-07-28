# Architecture Decision Records

## Назначение

Этот каталог содержит Architectural Decision Records (ADR).

ADR используется для фиксации важных архитектурных решений проекта Сфера.

Цели:

- сохранить историю решений;
- объяснить причины выбора архитектуры;
- предотвратить возврат к устаревшим подходам;
- обеспечить единое понимание архитектуры команды.


# Формат ADR

Каждое значимое решение должно иметь отдельный документ.


Структура:


```

docs/adr/

0001-architecture-principles.md

0002-decision-name.md

0003-decision-name.md

```


# Когда создавать ADR


ADR создаётся если решение влияет на:

- архитектуру системы;
- структуру проекта;
- границы доменных контекстов;
- технологический стек;
- взаимодействие модулей;
- правила разработки.


Примеры:


```

Выбор DDD

Переход на Application Services

Использование Repository Pattern

Выбор системы хранения файлов

Интеграция с внешними сервисами

```


# ADR Lifecycle


Каждый ADR имеет статус:


```

PROPOSED

ACCEPTED

SUPERSEDED

REJECTED

```


## PROPOSED


Решение рассматривается.


## ACCEPTED


Решение принято и используется.


## SUPERSEDED


Решение заменено новым ADR.


## REJECTED


Решение отклонено.


# Current ADRs


## ADR-0001

Файл:


```

0001-architecture-principles.md

```


Статус:


```

ACCEPTED

```


Тема:


```

Основные архитектурные принципы Sfera

```


Основные решения:


- использование DDD;
- Clean Architecture;
- разделение слоёв;
- Repository Pattern;
- Domain Events;
- независимость Domain Layer.


# Architecture Principles


## Domain First


Разработка начинается с бизнес-модели.


Правильный порядок:


```

Domain

↓

Application

↓

Infrastructure

↓

API

```


## Dependency Rule


Внутренние слои не зависят от внешних.


Разрешено:


```

API

↓

Application

↓

Domain

```


Запрещено:


```

Domain

↓

FastAPI

↓

SQLAlchemy

```


## Application Service Pattern


Application Layer является точкой выполнения бизнес-сценариев.


Пример:


```

API

↓

OrderApplicationService

↓

Order Aggregate

↓

Repository

```


## Repository Pattern


Domain определяет интерфейс хранения.


Пример:


```

OrderRepository

```


Infrastructure предоставляет реализацию:


```

SQLAlchemyOrderRepository

```


## Domain Events


Изменения важных состояний могут публиковать события.


Примеры:


```

OrderCreated

VerificationCompleted

PriceListActivated

```


# ADR Rules


Новый ADR должен содержать:


```

1. Context

2. Decision

3. Alternatives

4. Consequences

5. Status

```


# ADR Naming


Формат:


```

NNNN-short-description.md

```


Пример:


```

0002-storage-service.md

```


# Current Architecture Baseline


Версия:


```

Sfera v2.0 Architecture

```


Baseline tag:


```

v2.0-architecture

```


Основные решения:


```

✓ DDD

✓ Clean Architecture

✓ Application Services

✓ Repository Pattern

✓ Domain Events

✓ Dependency Injection

```


# Future ADRs


Планируемые решения:


```

ADR-0002

Storage Service Architecture

ADR-0003

Arshin Integration Strategy

ADR-0004

Audit Logging Architecture

ADR-0005

Document Generation Strategy

```


# Rule


Любое изменение, которое меняет архитектурное направление проекта, должно быть сначала описано в ADR.
```
