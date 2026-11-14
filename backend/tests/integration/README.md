# Isolated PostgreSQL integration-test database

This database is disposable and exists only for backend integration tests.

## Isolation guarantees

- Dedicated database: `sfera_test`.
- Dedicated test-only credentials; never reuse application credentials.
- PostgreSQL is published only on host loopback at `127.0.0.1:55432`.
- The Compose project has its own name and does not attach to the application Compose project.
- No host database directory or named volume is mounted.
- Do not change the URL below to point at a development or production database.

## Start the database

From `~/sfera/backend`, activate the project virtual environment first so the Alembic CLI and project dependencies are available:

```bash
source .venv/bin/activate
docker compose -f compose.integration.yaml up -d --wait
```

## Apply the application schema

The one-time `a6c8e1f3b520` data-reset migration intentionally requires the existing `alex/admin` account. A fresh integration database has no such account. Bootstrap a disposable placeholder account immediately before that migration; do not modify or bypass the production migration's safety guard.

Use the explicit test URL in the same shell:

```bash
export DATABASE_URL='postgresql+psycopg2://sfera_test:sfera_test_only@127.0.0.1:55432/sfera_test'

alembic upgrade 9f2a6c4d8e14

docker compose -f compose.integration.yaml exec -T postgres \
  psql -U sfera_test -d sfera_test -v ON_ERROR_STOP=1 <<'SQL'
INSERT INTO users (id, username, password_hash, is_active, role, archived)
VALUES (
    '00000000-0000-0000-0000-000000000001',
    'alex',
    'integration-test-placeholder-not-for-login',
    TRUE,
    'admin',
    FALSE
);
SQL

alembic upgrade head
alembic current
```

Expected current revision: `c2e5f7a9b310`.

The placeholder account exists only in the disposable database and is removed when the Compose container is torn down. It has no `user_roles` rows and is not a usable application login. The normal Alembic migration chain still executes in full, including the reset migration and its guard.

The schema is created through real migrations rather than `metadata.create_all()`, preserving migration-managed database behavior.

## Stop and remove the disposable database

After integration tests:

```bash
docker compose -f compose.integration.yaml down --volumes --remove-orphans
```

This removes the test container and its writable database layer. It does not address or modify any other PostgreSQL service.

The persistence integration fixture and test are a separate next step. Do not run the application backend against this test database.
