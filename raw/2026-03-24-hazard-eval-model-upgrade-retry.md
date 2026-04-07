---
project: field1st
repo: rtslabs/field1st
pr: 329
branch: fix/hazard-eval-504-retry
date: 2026-03-24
author: leo.brito
packages: [ai-orchestration]
tags: [testing, typescript]
related: []
answers: ["504 Gateway Timeout from hazard analysis process endpoint", "Vertex AI 429 RESOURCE_EXHAUSTED on gemini model", "Bounding boxes clustered at x=705 on hazard detection", "gemini-2.5-flash returns lazy full-image boxes instead of localizing hazards"]
---

# Fix hazard eval failures — upgrade model and add 5xx retry

## Motivation
Eval tests failed on DEV with 504 Gateway Timeout (Vertex AI rate limit hit on `gemini-3.1-pro-preview`) and on DEMO with poor bounding box quality (`gemini-2.5-flash` returned lazy full-image boxes at x=705 instead of localizing hazards).

## What changed
Upgraded `hazard-yxyx-format` test from `gemini-2.5-flash` to `gemini-3.1-pro-preview`. Added retry loop with 5s delay in `test-hazard.ts` when process endpoint returns 5xx or network error (max 2 attempts).

## Why this approach
- The flash model was too aggressive with bounding boxes. The pro-preview model already proved reliable in other tests.
- Retry on 5xx only — transient Vertex AI rate limits (429 -> 504) should retry, client errors (4xx) should fail immediately.

## Lessons
- Langfuse trace showed two consecutive 429 RESOURCE_EXHAUSTED errors from Vertex AI before the gateway timeout. The failure was upstream, not in our orchestration layer. Check Langfuse traces for upstream API failures before debugging orchestration code.
- `gemini-2.5-flash` has a tendency to return lazy bounding boxes (full-image coordinates) when rushed. Use `gemini-3.1-pro-preview` for tasks requiring precise localization.
- Add retries at the network fetch level, not after parsing — you may not get a parseable response on 5xx.

## If you're working on something similar
- Check Langfuse traces for upstream API failures before debugging orchestration code.
- Retry on 5xx but fail fast on 4xx — don't mask client errors with retries.
- Use `gemini-3.1-pro-preview` for tasks requiring precise bounding boxes or structured output.
