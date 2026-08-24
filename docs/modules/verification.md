# Модуль Verification

**Версия:** 1.1
**Дата актуализации:** 2026-07-16

---

# 1. Назначение

Verification реализует процесс поверки средств измерений в системе «Сфера».

Модуль предназначен для:

- регистрации результатов поверки;
- хранения данных о проведённой поверке;
- формирования результатов для ФГИС «Аршин»;
- контроля сроков действия поверки.

---

# 2. Место в бизнес-процессе

Поверка выполняется в рамках заказа:

```text
Customer

↓

Order

↓

OrderItem

↓

Verification
```

---

# 3. Основная сущность

```text
Verification
```

Verification является производственным результатом выполнения операции поверки.

---

# 4. Связи

Структура:

```text
OrderItem

↓

Verification

↓

ArshinExport
```

---

# 5. Основные данные Verification

Хранятся:

- дата поверки;
- срок действия;
- результат;
- методика;
- причина непригодности;
- исполнитель;
- статус экспорта.

---

# 6. Результаты поверки

Допустимые результаты:

```text
SUITABLE

UNSUITABLE
```

---

# 7. Правила результата

## SUITABLE

Пригодно:

- заполняется дата поверки;
- заполняется срок действия;
- разрешён экспорт в Аршин.

---

## UNSUITABLE

Непригодно:

- указывается причина;
- срок действия не указывается;
- результат экспортируется с причиной непригодности.

---

# 8. Методика поверки

Каждая поверка должна иметь методику.

Источник:

```text
VerificationMethod

или

Methodology
```

---

# 9. Domain Model

Основные компоненты:

```text
Verification Entity

VerificationResult Value Object

VerificationFactory

VerificationRepository

VerificationDomainService
```

---

# 10. Жизненный цикл

```text
CREATED

↓

IN_PROGRESS

↓

COMPLETED

↓

EXPORTED
```

---

# 11. Domain Events

События:

```text
VerificationCreated

VerificationCompleted

VerificationExported
```

---

# 12. Application Services

Основной сервис:

```text
VerificationService
```

Операции:

```text
Create Verification

Complete Verification

Export Verification
```

---

# 13. Repository

Интерфейс:

```text
VerificationRepository
```

Реализация:

```text
SQLAlchemyVerificationRepository
```

---

# 14. Аршин

Экспорт выполняется только если:

- поверка завершена;
- данные валидны;
- нет флага исключения;
- отсутствует ошибка подготовки.

---

# 15. Правила Аршин

Заполняются поля:

```text
A  - registry number

B  - serial number

C  - modification

E  - verification date

F  - valid until

H  - unsuitable reason

K  - methodology

N  - owner
```

Для составных средств:

```text
AF - Состав СИ
```

---

# 16. Ограничения

Запрещается:

- создавать поверку без OrderItem;
- изменять завершённую поверку;
- экспортировать непроверенные данные;
- удалять историю результатов.

---

# 17. Тестирование

Проверяются:

- создание поверки;
- корректность результатов;
- обязательность причины непригодности;
- расчёт срока действия;
- подготовка экспорта Аршин.

---

# 18. Главный принцип

Verification хранит юридически значимый результат поверки и должен обеспечивать полную воспроизводимость истории измерительного контроля.
