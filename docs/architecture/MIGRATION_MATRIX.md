# Sfera Migration Matrix

| Module | Legacy | Domain | Application Service | Repository | Infrastructure | API | Tests | Status |
|--------|--------|--------|---------------------|------------|----------------|-----|-------|--------|
| Organization | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED |
| Customer | removed | partial | partial | partial | partial | partial | partial | INCOMPLETE — Customer ↔ Organization use cases not migrated |
| Order | removed | partial | partial | ✓ | partial | ✓ | partial | INCOMPLETE — order still carries legacy payer organization |
| Material | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED |
| Warehouse | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED |
| Verification | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED |
| Repair | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED |
| Diagnostic | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED |
| PriceList | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED* |
| PriceListItem | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED* |
| Device | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED |
| Workflow | removed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | COMPLETED |

`*` Migration is complete. PriceList / PriceListItem have an isolated identifier-creation contract debt that must be resolved separately.

---

## Customer / Organization / Order business-flow correction

The previous matrix marked Customer and Order as fully migrated based on architectural layer presence. This was insufficient: the Customer ↔ Organization business relationship existed in persistence but was not exposed through Domain/Application/API/UI, while Order creation still copied a mandatory Organization from Customer.

The corrected business contract is recorded in:

- `docs/architecture/CUSTOMER_ORGANIZATION_SITE_MODEL.md`
- `docs/architecture/CUSTOMER_SERVICE_DESIGN.md`

Customer and Order remain incomplete until the relationship management and order decoupling use cases are implemented and validated.

---

# Current Architecture

```text
API
↓
Application Service
↓
Domain
↓
Repository Interface
↑
Infrastructure Repository
↓
Database
```

---

# Migration Standard

Каждый новый функционал реализуется исключительно через Application use case и repository abstraction:

```text
API
↓
Application Service / Command
↓
Domain
↓
Repository Interface
↑
Infrastructure Repository
↓
Database
```

Правила:

- Domain не зависит от внешних слоев.
- Application не зависит от Infrastructure.
- API не содержит бизнес-логики.
- API не обращается к Repository или Database напрямую.
- SQLAlchemy используется только в Infrastructure.
- Legacy CRUD запрещён для новых use cases.
- Новые use cases создаются через Application Services.
- Domain state changes принадлежат Domain entities/domain services.
- Infrastructure отвечает за persistence и mapping.

---

# Completed Architecture Checkpoints

Архитектурные проверки подтверждают направление зависимостей и удаление legacy CRUD. Они не являются доказательством полноты переноса каждого бизнес-сценария. Статус модуля определяется также соответствием его Domain/Application/API/UI фактическому бизнес-контракту.
