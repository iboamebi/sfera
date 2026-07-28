# Sfera Internal Engines

## Назначение

Каталог описывает внутренние механизмы и технические подсистемы проекта Сфера.

Engines являются инфраструктурными компонентами, обеспечивающими работу системы.

Основные задачи:

- выполнение технических операций;
- интеграция с внешними системами;
- обработка внутренних процессов;
- обеспечение сервисных функций.


# Architecture Position


Engines находятся вне Domain Layer.


Структура:


```

API

↓

Application

↓

Domain

↓

Infrastructure

↓

Engines

```


Engines не содержат бизнес-правила.

Они предоставляют технические возможности для Application и Infrastructure слоёв.


# Engine Principles


## Separation of Concerns


Каждый engine отвечает только за одну техническую область.


Пример:


```

Storage Engine

```
отвечает за файлы
```

Document Engine

```
отвечает за генерацию документов
```

Integration Engine

```
отвечает за внешние системы
```

```


---

## Dependency Rule


Domain не зависит от Engines.


Правильно:


```

Application

↓

Engine Interface

↓

Engine Implementation

```


Неправильно:


```

Domain

↓

External Engine

```


---

# Planned Engines


## Storage Engine


Статус:


```

PLANNED

```


Назначение:

Управление хранением больших бинарных объектов.


Использование:


- документы;
- фотографии;
- сканы;
- результаты измерений;
- вложения.


Основные функции:


```

upload()

download()

delete()

get_metadata()

```


Хранилище:


```

External Storage

*

Metadata Database

```


---

# Document Engine


Статус:


```

PLANNED

```


Назначение:

Генерация документов.


Использование:


- свидетельства поверки;
- акты;
- договоры;
- коммерческие предложения.


Функции:


```

generate()

render()

export()

```


---

# Arshin Integration Engine


Статус:


```

PLANNED

```


Назначение:

Интеграция с ФГИС Аршин.


Функции:


```

prepare_export()

validate_data()

send()

track_status()

```


Основные правила:


Экспортируются:


```

только завершённые поверки

```


Не экспортируются:


```

do_not_export = true

```


---

# Audit Engine


Статус:


```

PLANNED

```


Назначение:

Аудит действий пользователей.


Функции:


```

record_event()

search_history()

export_log()

```


События:


```

UserAction

EntityChanged

StatusChanged

```


---

# Notification Engine


Статус:


```

PLANNED

```


Назначение:

Уведомления пользователей.


Каналы:


```

Email

SMS

Internal Notification

Webhook

```


---

# Integration Engine


Статус:


```

PLANNED

```


Назначение:

Внешние интеграции.


Возможные системы:


```

ФГИС Аршин

Бухгалтерские системы

CRM

Платёжные системы

```


---

# Engine Development Rules


Перед созданием нового engine:


```

1. определить техническую ответственность

2. создать интерфейс

3. определить Application integration point

4. создать реализацию

5. добавить тесты

6. добавить документацию

```


---

# Testing


Engines должны тестироваться отдельно.


Типы тестов:


```

Unit Tests

Integration Tests

External Service Tests

```


Внешние системы должны заменяться mock/stub реализациями.


---

# Current Status


```

Storage Engine          PLANNED

Document Engine         PLANNED

Arshin Engine           PLANNED

Audit Engine            PLANNED

Notification Engine     PLANNED

Integration Engine      PLANNED

```


# Future Architecture


Планируемая структура:


```

backend/app/

├── engines/

│
├── storage/

├── documents/

├── arshin/

├── audit/

└── notifications/

```


# Version


Current architecture:


```

Sfera v2.0 Architecture

```
```
