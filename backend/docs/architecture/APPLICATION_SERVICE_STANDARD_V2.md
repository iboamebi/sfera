# Application Service Standard v2.0

Date:

2026-08-05

Baseline:

Sfera Architecture v2.0

---

## Purpose

Application Service coordinates application use cases.

Application Service is responsible for:

- executing use cases;
- coordinating domain objects;
- validating application-level conditions;
- calling repository interfaces;
- managing application exceptions.

Application Service is not responsible for:

- database access;
- ORM operations;
- API concerns;
- infrastructure details.

---

# Architecture Flow

Standard flow:
API
↓
Command / Query
↓
Application Service
↓
Domain Entity / Domain Service
↓
Repository Interface
↓
Infrastructure Repository
↓
Database


---

# Application Service Rules

## Rule 1. One method = one use case

Application Service methods must represent business actions.

Correct:

```python
approve()
reject()
complete()
reserve()
activate()

Avoid:

update_status()
save_changes()
process()
Rule 2. Commands for state changes

Operations changing domain state should use Commands.

Example:

API
 ↓
ApproveVerificationCommand
 ↓
VerificationApplicationService.approve()
 ↓
Domain Entity.approve()
 ↓
Repository.save()
Rule 3. Domain owns business state changes

Application Service coordinates.

Domain Entity decides.

Correct:

entity.complete()
repository.save(entity)

Incorrect:

entity.status = "COMPLETED"
repository.save(entity)
Rule 4. Repository access only from Application

Allowed:

Application Service
        ↓
Repository Interface

Forbidden:

API
 ↓
Repository

or:

Domain
 ↓
Repository implementation
Rule 5. No Infrastructure dependencies

Application layer must not import:

SQLAlchemy;
ORM models;
database sessions;
infrastructure repositories.

Forbidden:

from sqlalchemy.orm import Session
from app.models.*
from app.infrastructure.*
Rule 6. Application Exceptions

Application-level errors belong to Application layer.

Examples:

CustomerNotFoundApplicationError
WorkflowNotFoundApplicationError
VerificationNotFoundApplicationError

Domain errors must not leak directly through API.

Migration Strategy

Existing migrated modules may contain CRUD-style Application Services.

Migration path:

Existing Application Service
        ↓
Identify business operations
        ↓
Create Commands
        ↓
Move state changes to Domain
        ↓
Remove generic CRUD methods
        ↓
Validate tests
Current Migration Status

Completed use-case style modules:

Workflow
Repair
Verification

Partially migrated:

Customer
Material
Organization
Diagnostic
Warehouse
Order
PriceList
Validation Checklist

Before completing migration:

 no Infrastructure imports
 no ORM imports
 state changes delegated to Domain
 Commands created for mutations
 Application exceptions isolated
 tests updated
 API contains no business logic
Goal

Move all Application Services from CRUD-oriented operations to explicit business use cases while preserving DDD/Clean Architecture boundaries.
