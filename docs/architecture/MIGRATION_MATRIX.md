# Architecture Migration Matrix

Краткая матрица контроля перехода модулей от CRUD к DDD/Clean Architecture.

Подробный статус миграции:
`docs/MIGRATION_STATUS.md`

| Module       | CRUD   | Domain | Service | Repository | API | Status      |
| ------------ | ------ | ------ | ------- | ---------- | --- | ----------- |
| PriceList    | legacy | ✓      | ✓       | ✓          | ✓   | IN_PROGRESS |
| Customer     |        |        |         |            |     |             |
| Instrument   |        |        |         |            |     |             |
| Verification |        |        |         |            |     |             |
