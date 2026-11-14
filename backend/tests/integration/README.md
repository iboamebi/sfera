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

From `~/sfera/backend`:

```bash
docker compose -f compose.integration.yaml up -d --wait
```

## Apply the application schema

Use the explicit test URL in the same shell:

```bash
export DATABASE_URL='postgresql+psycopg2://sfera_test:sfera_test_only@127.0.0.1:55432/sfera_test'
alembic upgrade head
```

The normal Alembic migration chain is used; this avoids a schema created by `metadata.create_all()` that would omit migration-managed database behavior.

## Stop and remove the disposable database

After integration tests:

```bash
docker compose -f compose.integration.yaml down --volumes --remove-orphans
```

This removes the test container and its writable database layer. It does not address or modify any other PostgreSQL service.

The persistence integration fixture and test are a separate next step. Do not run the application backend against this test database.
