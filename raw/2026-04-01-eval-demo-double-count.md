---
project: field1st
repo: rtslabs/field1st
pr: 381
branch: fix/eval-demo-double-count
date: 2026-04-01
author: leo.brito
packages: [ai-orchestration]
tags: [ci-cd, testing]
related: []
answers: ["Eval tests show double count like 76/80 instead of 39/40", "DEMO eval tests include DEV results", "Stale .current-run-id marker causes test aggregation across environments"]
---

# Fix DEMO eval tests joining DEV run ID

## Motivation
The daily AI integration workflow runs eval tests against DEV, then DEMO. DEMO tests were incorrectly appending to the DEV run, causing test counts to double (e.g., 76/80 shown instead of 39/40 for DEMO).

## What changed
Added `rm -f test-artifacts/latest/.current-run-id` between DEV and DEMO test runs in `.github/workflows/ai-integration-daily.yml`.

## Why this approach
The `.current-run-id` marker persists across environments within a single workflow execution. Clearing it forces DEMO to start a fresh run instead of joining DEV's run.

## Lessons
The eval test harness uses `.current-run-id` to group tests into runs. When multiple environments run sequentially in the same workflow, the marker must be cleared between them to prevent cross-environment aggregation.

## If you're working on something similar
- Look for `.current-run-id` in `test-artifacts/latest/` if test counts seem aggregated.
- Clear the marker between environment steps: `rm -f test-artifacts/latest/.current-run-id`.
- Check other workflows with multi-environment eval runs for the same pattern.
