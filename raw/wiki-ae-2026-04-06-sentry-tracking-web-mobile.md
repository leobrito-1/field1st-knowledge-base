---
project: field1st
repo: rtslabs/field1st
jira: F1-262
pr: 415
branch: feature/F1-262-enable-sentry-tracking
date: 2026-04-06
author: andy.ewald
packages: [web, mobile]
tags: [web, mobile, security]
related: []
answers: ["Sentry not receiving events", "production errors not tracked", "cant filter Sentry by tenant", "Sentry environment tag missing", "web Sentry broken in production"]
files: ["packages/mobile/src/core/App.tsx", "packages/mobile/src/shared/auth/useLogin.tsx", "packages/mobile/src/shared/types/react-native-dotenv.d.ts", "packages/mobile/src/storm/App.tsx", "packages/web/packages/field-first/src/index.tsx"]
---

# Enable Sentry tracking for web and mobile environments

## Motivation
Sentry was silently disabled on web production due to case mismatch between env vars (lowercase prod) and switch statement (uppercase checks). Mobile lacked environment tags for filtering.

## What changed
Web: case-insensitive env switch via toUpperCase(), new field1st-web Sentry project, environment and site tags. Mobile: updated ingest hosts, added SENTRY_ENVIRONMENT to all env files, site tag with API hostname for tenant filtering.

## Why this approach
- Case-insensitive switch handles env var inconsistencies across deployment systems.
- environment tag enables filtering by deployment target.
- site tag (hostname) enables filtering by tenant in multi-tenant SaaS.

## Lessons
- Environment variable case is not guaranteed across deployment systems. Normalize with toUpperCase() before comparisons.
- Multi-tenant apps need per-customer error filtering. Hostname tag is cheap and effective.
- Missing await on async callbacks prevents error reporting tools from seeing the error. Always await.
- Sentry tags must be set before errors occur — post-error tagging doesn't retroactively tag.

## If you're working on something similar
- Normalize env var case before comparing.
- Set Sentry environment tag at initialization.
- Tag multi-tenant apps with site/workspace hostname.
- Always await async callbacks that should propagate errors.
