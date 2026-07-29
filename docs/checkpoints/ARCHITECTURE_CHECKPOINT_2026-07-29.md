Architecture checkpoint

Date:
2026-07-29

Status:
CRUD → DDD migration in progress

Completed:

[✓] Project Constitution 2.0
[✓] Layer standards
[✓] PriceList migration example

In progress:

[ ] Complete domain migration
[ ] Repository standardization
[ ] Remove legacy CRUD

Migration rule:

Legacy CRUD remains only as reference.
New features must use:

Domain
 ↓
Application
 ↓
Repository
 ↓
Infrastructure
 ↓
API

Current migrated modules:

PriceList

Next modules:
...
