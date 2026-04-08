---
project: field1st
repo: rtslabs/field1st
pr: 192
branch: fix/migration-bootstrap
date: 2026-03-07
author: leo.brito
packages: [ai-orchestration]
tags: [infra]
related: []
answers: ["migration fails with schema rag does not exist", "pgvector extensions not created on RDS", "rag.embeddings table does not exist on new deployment", "migrations work on Docker Compose but fail on managed database"]
files: ["packages/ai-orchestration/db/migrations/00000000000000_bootstrap_rag_schema.sql"]
---

# Bootstrap migration for managed database environments

## Motivation
New production deployments on managed databases (RDS) failed with `schema "rag" does not exist` because the `rag` schema and base tables were only created by Docker's `docker-entrypoint-initdb.d` mechanism. That mechanism only runs on fresh Docker Compose containers, not on managed databases.

## What changed
Added a bootstrap migration (`00000000000000_bootstrap_rag_schema.sql`) that sorts before all others and creates the baseline: extensions (`pgcrypto`, `vector`), `rag` schema, `rag.embeddings` table, `rag.touch_updated_at()` function, and legacy `rag.ingested_files` table.

## Why this approach
- Fully idempotent (`IF NOT EXISTS` / `OR REPLACE`) so it's a no-op on existing environments where the init script already ran.
- Migration filename `00000000000000_...` sorts before all existing migrations lexicographically.
- Mirrors `db/init/01_embeddings.sql` exactly to ensure Docker Compose and managed DB environments have identical schema.

## Lessons
- `docker-entrypoint-initdb.d` only runs on Docker Compose, not RDS/managed DBs. Never assume Docker init scripts will run in production. Managed databases require migrations to handle schema bootstrapping.
- Verified by spinning up a bare `postgis11-pgvector:latest` container with no init scripts, running migrations, and confirming all 18 applied successfully. Re-running confirmed idempotency.

## If you're working on something similar
- Test migrations against a fresh database with no Docker init scripts: `docker run -d --name pgvector-clean-test -e POSTGRES_DB=rag -e POSTGRES_USER=rag_user -e POSTGRES_PASSWORD=rag_password -p 5499:5432 postgis11-pgvector:latest`.
- Run `node scripts/run-migrations.mjs` against the clean database. Re-run to confirm idempotency.
- Check for schema references in `db/init/` scripts and mirror them in a bootstrap migration that sorts first.
