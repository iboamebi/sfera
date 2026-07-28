# Repository Layer Standard

## Версия

v1.0

## Назначение

Настоящий документ определяет единый стандарт реализации Repository слоя проекта «Сфера».

После утверждения документа все новые Repository создаются исключительно по данному шаблону.

---

# Место Repository в архитектуре

```text
HTTP

 │

 ▼

FastAPI Router

 │

 ▼

Application Service

 │

 ▼

Repository Interface

 │

 ▼

Infrastructure Repository

 │

 ▼

CRUD

 │

 ▼

SQLAlchemy

 │

 ▼

PostgreSQL
```

---

# Ответственность Repository

Repository отвечает только за доступ к данным.

Repository:

- получает данные;
- сохраняет данные;
- обновляет данные;
- удаляет данные;
- ничего не знает о HTTP;
- ничего не знает о FastAPI;
- ничего не знает о бизнес-правилах.

---

# Repository запрещено

Repository НЕ должен:

- выполнять проверки бизнес-логики;
- менять статус заказа;
- рассчитывать стоимость;
- принимать решения;
- работать с событиями;
- обращаться к другим Repository.

---

# Базовый класс

Все Repository наследуются от BaseRepository.

```python
class CustomerRepository(BaseRepository):

    def __init__(self, db):
        super().__init__(
            db,
            customer_crud,
        )
```

Порядок параметров всегда одинаковый:

```python
super().__init__(
    db,
    crud,
)
```

Изменение порядка запрещено.

---

# Repository Interface

Каждый модуль имеет собственный интерфейс.

Пример:

```python
class CustomerRepositoryInterface:

    def get(self, customer_id):
        ...

    def get_all(self):
        ...

    def save(self, customer):
        ...

    def archive(self, customer):
        ...
```

Application Service работает только через интерфейс.

---

# CRUD

Repository является единственным слоем, которому разрешено использовать CRUD.

```text
Application Service

        │

        ▼

Repository

        │

        ▼

CRUD
```

CRUD напрямую из Service не вызывается.

---

# SQLAlchemy

Repository работает через Session.

```python
class CustomerRepository(BaseRepository):

    def get(self, customer_id):
        return self.crud.get(
            self.db,
            customer_id,
        )
```

Session никогда не передается выше Repository.

---

# Работа с несколькими Repository

Если необходимо использовать несколько Repository одновременно, это делает Application Service.

Пример:

```text
OrderService

      │

      ├── CustomerRepository

      │

      ├── OrderRepository

      │

      └── WarehouseRepository
```

Repository между собой не взаимодействуют.

---

# Unit of Work

Repository не выполняет commit().

Repository не открывает транзакции.

Repository не вызывает rollback().

Все транзакции выполняются через Unit of Work.

---

# Domain Events

Repository не создает события.

Repository не публикует события.

Все события создаются в Application Service либо Domain.

---

# Возвращаемые объекты

Repository возвращает:

- Domain Entity;
- Aggregate;
- Value Object;
- коллекции объектов.

Repository никогда не возвращает HTTP Response.

---

# Исключения

Repository может выбрасывать только технические ошибки.

Например:

- DatabaseError;
- IntegrityError;
- OperationalError.

Доменные исключения создаются выше.

---

# Именование

Используется единый стиль.

```text
CustomerRepository

OrderRepository

RepairRepository

VerificationRepository

WarehouseRepository
```

CRUD:

```text
customer_crud

order_crud

repair_crud
```

---

# Структура каталогов

```text
app/

├── infrastructure/

│   ├── customer/

│   │   └── customer_repository.py

│   ├── order/

│   │   └── order_repository.py

│   ├── repair/

│   │   └── repair_repository.py

│   └── ...
```

---

# Проверка качества

Каждый Repository должен удовлетворять следующим требованиям:

- наследуется от BaseRepository;
- использует единый конструктор;
- работает только через CRUD;
- не содержит бизнес-логики;
- не использует FastAPI;
- не использует HTTP;
- не выполняет commit();
- не выполняет rollback();
- покрыт тестами.

---

# Итоговый стандарт

Repository является инфраструктурным адаптером между Application Service и SQLAlchemy.

После утверждения настоящего документа любые отклонения от данного стандарта считаются нарушением архитектуры проекта «Сфера».
