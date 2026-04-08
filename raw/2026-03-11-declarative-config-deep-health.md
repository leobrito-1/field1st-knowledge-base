---
project: field1st
repo: rtslabs/field1st
pr: 200
branch: rework/env-guard
date: 2026-03-11
author: leo.brito
packages: [ai-orchestration]
tags: [typescript, infra, testing]
related: []
answers: ["ai-orchestration config validation fails silently", "missing env var not caught until runtime", "health check only returns ok/down without dependency details", "operators cannot verify AWS/GCS/Postgres connectivity before deploying"]
files: ["packages/ai-orchestration/src/config-schema.ts", "packages/ai-orchestration/src/config.ts", "packages/ai-orchestration/src/health/probes.ts", "packages/ai-orchestration/src/health/types.ts", "packages/ai-orchestration/src/mastra/index.ts"]
---

# Declarative config validation and deep health checks

## Motivation
The old `config.ts` was 270 lines of imperative if/else checks that only verified env vars were present, not that credentials or connections actually worked. Operators deploying to new environments had no way to quickly verify that all dependencies (Postgres, SQS, GCS, Vertex, OpenAI, Langfuse) were reachable.

## What changed
Replaced hand-written config validation with a declarative Zod schema in `config-schema.ts`. Added a deep health check mode to `/healthz` that verifies each dependency actually works — probes run in parallel with individual 5s timeouts, returning ok/degraded/down per probe.

## Why this approach
- Zod schemas are declarative and provide structured error messages on validation failure.
- Separating schema into `config-schema.ts` allows tests to import it without triggering validation side effects.
- Critical probes (postgres, sqs, gcs) cause "down" status; non-critical failures (openai, langfuse) cause "degraded"; unconfigured probes show "skip".
- Default `/healthz` behavior unchanged (fast liveness for load balancers).

## Lessons
- Separate schema declaration from validation execution. Tests import `config-schema.ts` without triggering the top-level validation that runs when importing `config.ts`.
- 27 config tests caught edge cases (numeric bounds, boolean transforms, cross-field rules, defaults) that would have been missed in a straight port from imperative to Zod.
- Deep health probes verify dependencies work, not just that env vars exist. `GET /healthz?deep=true` runs all probes in parallel.

## If you're working on something similar
- Separate schema from validation execution — export from `config-schema.ts`, import in `config.ts` to run on load.
- Use individual timeouts per probe (5-10s) and run with `Promise.allSettled()` — prevents slow dependencies from blocking the entire check.
- Classify probes as critical vs non-critical. Critical failures return "down"; non-critical return "degraded".
- Run `GET /healthz?deep=true` in deployed environments to verify all probes reach dependencies.
