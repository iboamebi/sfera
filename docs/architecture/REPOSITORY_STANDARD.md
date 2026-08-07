# Sfera Repository Standard

## Назначение

Repository Layer обеспечивает абстракцию доступа к данным между Domain и Infrastructure слоями.

Repository Interface находится в Domain и описывает контракт работы с агрегатами.

---

## Dependency Rule

Допустимое направление зависимостей:


API
↓
Application Service
↓
Domain Repository Interface
↑
Infrastructure Repository
↓
Database


Domain Repository Interface:

- не зависит от SQLAlchemy;
- не зависит от ORM моделей;
- не зависит от Infrastructure;
- не содержит запросов к базе данных.

---

## Repository Interface Rules

Каждый repository interface:

- находится в:


app/domains/<module>/repositories/


- является абстрактным контрактом;
- наследуется от `ABC`;
- содержит только методы, необходимые конкретному агрегату.

Пример:

```python
from abc import ABC, abstractmethod


class ExampleRepository(ABC):
    """Repository interface."""

    @abstractmethod
    def get(self, entity_id):
        raise NotImplementedError

    @abstractmethod
    def save(self, entity):
        raise NotImplementedError
Repository Methods

Нет обязательного общего CRUD-контракта.

Набор методов определяется бизнес-операциями агрегата.

Допустимые методы:

get()
get_all()
save()
delete()
find_by_*
get_active()
get_by_*

Примеры:

Device:

get()
save()

Warehouse:

get()
get_by_material()
save()

Workflow:

get_workflow()
get_instance()
save_instance()
Generic Repository

app.shared.base.repository.Repository[T]

используется только как базовый marker type.

Он не определяет обязательные методы.

Причина:

разные агрегаты имеют разные persistence use cases.

Infrastructure Implementation

Реализация repository находится только в:

app/infrastructure/<module>/

Infrastructure repository:

реализует Domain Repository Interface;
работает с SQLAlchemy;
использует Mapper для преобразования:
ORM Model
    ↓
Mapper
    ↓
Domain Entity
Prohibited

Запрещено:

импортировать Infrastructure в Domain;
импортировать SQLAlchemy в Domain;
использовать ORM модели в Repository Interface;
добавлять бизнес-логику в Infrastructure Repository;
создавать новые CRUD repositories.
Migration Rule

При добавлении нового функционала:

Application Service
        ↓
Repository Interface
        ↓
Infrastructure Repository
        ↓
Database

Legacy CRUD не используется.
