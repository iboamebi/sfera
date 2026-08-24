# Документация проекта «Сфера»

**Версия:** 1.1
**Дата актуализации:** 2026-07-16

---

# 1. Назначение

Данный каталог содержит техническую и архитектурную документацию проекта «Сфера».

Документация является частью исходного кода проекта.

---

# 2. Структура документации

```text
docs/

├── README.md

├── architecture/

├── database/

├── modules/

├── api/

└── deployment/
```

---

# 3. Architecture

Каталог:

```text
docs/architecture/
```

Содержит основные архитектурные решения.

Файлы:

```text
project_constitution.md

project_structure.md

domain_layer.md

application_layer.md

infrastructure_layer.md

api_layer.md

testing_strategy.md
```

---

# 4. Database

Каталог:

```text
docs/database/
```

Содержит документацию базы данных.

Файлы:

```text
schema.md

migrations.md
```

---

# 5. Modules

Каталог:

```text
docs/modules/
```

Содержит описание бизнес-модулей.

Основные модули:

```text
order.md

device.md

verification.md

diagnostic.md

repair.md

warehouse.md

arshin.md

pricing.md

document.md

user_management.md

audit.md
```

---

# 6. API

Каталог:

```text
docs/api/
```

Содержит описание внешнего интерфейса.

Файлы:

```text
rest_api.md

authentication.md
```

---

# 7. Deployment

Каталог:

```text
docs/deployment/
```

Содержит инструкции эксплуатации.

Файлы:

```text
environment.md

backup.md
```

---

# 8. Правила изменения документации

Архитектурные изменения требуют:

1. Обновления соответствующего документа.
2. Проверки влияния на существующие модули.
3. Фиксации изменения в Git.

---

# 9. Источник истины

Основными документами являются:

```text
project_constitution.md

project_structure.md

domain_layer.md
```

При конфликте решений приоритет имеют эти документы.

---

# 10. Версионирование

Документация изменяется вместе с кодом.

Каждое значимое изменение должно сопровождаться:

- обновлением версии;
- описанием изменения;
- Git commit.

---

# 11. Главный принцип

Документация проекта «Сфера» является живой частью системы и должна отражать её текущее архитектурное состояние.
