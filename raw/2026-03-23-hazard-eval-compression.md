---
project: field1st
repo: rtslabs/field1st
pr: 307
branch: fix/bedrock-image-compression-threshold
date: 2026-03-23
author: leo.brito
packages: [ai-orchestration]
tags: [testing, typescript]
related: [2026-03-23-bedrock-converse-unification]
answers: ["Hazard eval Slack notification showing 0/0 passed instead of 5/5", "Anthropic rejected 5.03 MB JPEG as 6.7 MB after Converse API overhead", "Vitest test results reset between test files"]
files: ["packages/ai-orchestration/src/mastra/features/hazard/workflows/hazard-bedrock-config.ts", "packages/ai-orchestration/src/mastra/features/hazard/workflows/hazard-bedrock-image.ts", "packages/ai-orchestration/src/mastra/features/shared/vertex-fallback-chain.ts"]
---

# Hazard eval result accumulation and image compression fixes

## Motivation
After the Bedrock Converse unification (#303), the daily hazard eval Slack notification reported `0/0 passed` instead of `5/5 passed`, and images around 5 MB were still hitting Anthropic's post-overhead limit despite passing the pre-check threshold.

## What changed
Replaced in-memory test result accumulation with a shared JSONL file on disk. Lowered the Bedrock image compression threshold from 5 MB to 3.75 MB to account for Converse API overhead.

## Why this approach
- Vitest creates isolated module scope per test file, so in-memory state (`allResults` array) reset between test files. The last file overwrote `latest/summary.json` with its partial count.
- JSONL on disk lets all test files append to the same results file.
- 5 MB raw JPEG became 6.7 MB after Converse API encoding overhead. 3.75 MB threshold ensures compression fires before the request is sent.

## Lessons
- Module state is per-file in Vitest. `artifact-storage.ts` exported `let allResults: TestResult[] = []` expecting all test files to share it. Each file got its own instance. Solution: shared file on disk (`results.jsonl`).
- API overhead is non-trivial. A 5.03 MB JPEG was rejected as 6.7 MB. Always budget at least 25% headroom below stated limits when dealing with multipart/base64/JSON-wrapped binary payloads.

## If you're working on something similar
- Verify test result aggregation across multiple Vitest files by running the full suite and checking `latest/summary.json`.
- Use `packages/ai-orchestration/eval-tests/helpers/artifact-storage.ts` as the single source of truth for test results. Never bypass `saveTestResult()`.
- When setting image size thresholds for external APIs, budget 25-30% below the documented limit for encoding overhead.
