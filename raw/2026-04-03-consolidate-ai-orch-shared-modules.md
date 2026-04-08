---
project: field1st
repo: rtslabs/field1st
jira: F1-250
pr: 394
branch: feature/F1-250-ai-orch-shared
date: 2026-04-03
author: leo.brito
packages: [ai-orchestration]
tags: [typescript, infra, security]
related: []
answers: ["process.env is undefined in ai-orchestration at runtime", "ai-orchestration has multiple pg Pool instances", "Stack traces leaking in chat 500 responses", "Auth token cache growing unbounded in memory"]
files: ["packages/ai-orchestration/src/config-schema.ts", "packages/ai-orchestration/src/mastra/features/ai-settings/sql.ts", "packages/ai-orchestration/src/mastra/features/auth/auth.ts", "packages/ai-orchestration/src/mastra/features/chatv2/chat-v2-route.ts", "packages/ai-orchestration/src/mastra/features/chatv2/guardrails/guardrails-agent.ts"]
---

# Consolidate ai-orchestration shared modules and env validation

## Motivation
The ai-orchestration codebase had 35 files reading `process.env` directly (bypassing the Zod schema), 3 separate pg Pool instances, 3 image-fetch functions with inconsistent SSRF/timeout handling, and 26 env vars defined but never deployed. Each new AI provider added correct code in isolation but duplicated setup patterns.

## What changed
Created shared modules for timeout, Vertex AI bootstrap, and image fetching. Trimmed env schema from 55 to 29 vars. Replaced 35 `process.env` reads with validated `env` import. Consolidated 3 pg Pools into one. Added SSRF protection to control-viz image fetching. Capped auth token cache at 1000 entries with LRU eviction. Removed stack traces from chat 500 responses.

## Why this approach
- Single env validation boundary prevents runtime undefined errors and fails fast at startup
- Shared modules prevent copy-paste divergence — one fix applies everywhere
- LRU cache cap prevents memory leaks in long-running processes
- SSRF guard blocks internal network access via user-supplied URLs

## Lessons
- 35 files bypassed Zod validation with direct `process.env` reads, causing runtime `undefined` errors. Centralize env validation at startup — don't trust `process.env` at call sites. Created `packages/ai-orchestration/src/env.ts` wrapper.
- 3 separate `pg.Pool()` instances caused connection pool fragmentation. Database pools should be singletons — grep for `new Pool(` before adding new DB code.
- Auth token cache grew unbounded. All in-memory caches need size bounds and eviction policies, even if "users never have that many tokens."
- Control-viz fetched user-supplied image URLs without SSRF protection. Any user-controlled URL passed to `fetch()` needs SSRF validation.

## If you're working on something similar
- Run `rg 'process\.env\.' packages/ai-orchestration/src/ --type ts` to find direct env reads — replace with `env` import from `packages/ai-orchestration/src/env.ts`.
- Search for `new Pool(` before adding DB code — use `packages/ai-orchestration/src/mastra/shared/db/pool.ts`.
- Check `vitest.setup-env.ts` when adding new env vars — CI needs test defaults for Zod validation to pass.
- Grep for `fetch(.*http` to find SSRF risks — use `assertSafePublicHttpsImageUrl()` before user-controlled fetches.
