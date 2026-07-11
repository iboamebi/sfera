# Architecture Checklist

## Domain

- [ ] Нет SQLAlchemy
- [ ] Нет FastAPI
- [ ] Нет Pydantic
- [ ] Нет CRUD
- [ ] Нет ORM

## Aggregate

- [ ] Один Aggregate Root
- [ ] Инварианты соблюдаются
- [ ] Нет прямого изменения состояния извне

## Repository

- [ ] Только интерфейс
- [ ] Нет SQL

## Application

- [ ] Оркестрирует сценарий
- [ ] Не содержит бизнес-правил

## Infrastructure

- [ ] SQLAlchemy
- [ ] CRUD
- [ ] PostgreSQL

## API

- [ ] Только HTTP
- [ ] Только DTO

## Tests

- [ ] Unit
- [ ] Integration
