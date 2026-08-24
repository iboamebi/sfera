# База данных

Версия: 1.1

---

# СУБД

PostgreSQL

Используется UUID в качестве первичных ключей.

Все изменения структуры выполняются исключительно через Alembic.

---

# Общие правила

Каждая таблица наследует BaseModel.

Во всех таблицах присутствуют поля:

- id
- created_at
- updated_at
- archived

---

# Основные таблицы

## organizations

Организации.

---

## customers

Заказчики.

Связь:

```
Organization
    │
    ▼
Customer
```

---

## orders

Заказы.

Связь:

```
Customer
    │
    ▼
Order
```

---

## order_items

Позиции заказа.

Связь:

```
Order
    │
    ▼
OrderItem
```

---

## instruments

Средства измерений.

---

## instrument_types

Типы средств измерений.

---

## instrument_labels

Маркировки средств измерений.

---

## verifications

Результаты поверок.

---

## methodologies

Методики поверки.

---

## arshin_exports

История выгрузок в Аршин.

---

## diagnostics

Диагностика.

---

## repairs

Ремонт.

---

## production_movements

История прохождения заказа по производству.

---

## materials

Материалы.

---

## warehouses

Склады.

---

## warehouse_stocks

Остатки материалов.

---

## warehouse_movements

Движение материалов.

---

## documents

Документы.

---

## document_templates

Шаблоны документов.

---

## users

Пользователи.

---

## roles

Роли.

---

## permissions

Права доступа.

---

## role_permissions

Связь ролей и прав.

---

## user_roles

Связь пользователей и ролей.

---

## audit_logs

Журнал аудита.

---

# Основные связи

```
Organization
    │
    ▼
Customer
    │
    ▼
Order
    │
    ▼
OrderItem
```

```
OrderItem
    ├── Verification
    ├── Diagnostic
    ├── Repair
    └── Instrument
```

```
Verification
    ├── Methodology
    └── ArshinExport
```

```
Warehouse
    ├── WarehouseStock
    └── WarehouseMovement
            │
            ▼
        Material
```

---

# Индексация

Индексируются:

- все внешние ключи;
- номера заказов;
- серийные номера;
- регистрационные номера;
- артикулы;
- коды;
- активные статусы;
- поля поиска.

---

# Удаление данных

Физическое удаление допускается только для зависимых сущностей.

Основные сущности используют логическое удаление через поле:

```
archived
```

---

# Миграции

Все изменения структуры базы данных оформляются отдельной миграцией Alembic.

Редактирование существующих миграций после попадания в репозиторий запрещено.

---

# Наименование объектов

Таблицы:

- множественное число;
- snake_case.

Поля:

- snake_case.

Внешние ключи:

```
<entity>_id
```

Примеры:

```
customer_id
order_id
instrument_id
warehouse_id
```
