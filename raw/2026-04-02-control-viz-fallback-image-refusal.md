---
project: field1st
repo: rtslabs/field1st
pr: 389
branch: fix/control-viz-fallback-robustness
date: 2026-04-02
author: leo.brito
packages: [ai-orchestration]
tags: [typescript, infra]
related: [2026-04-02-gpt-image-fallback-control-viz]
answers: ["Gemini preview model returning text instead of image", "No generated image in response from Vertex AI", "Fallback chain dying on first tier without trying alternates", "Model returned 15 text tokens instead of image despite responseModalities IMAGE"]
files: ["packages/ai-orchestration/src/mastra/features/hazard-control/workflows/control-visualization-workflow.ts", "packages/ai-orchestration/src/mastra/features/hazard-control/workflows/control-viz-utils.ts", "packages/ai-orchestration/src/mastra/features/shared/vertex-error-classification.ts"]
---

# Robust control-viz fallback for image refusal and timeouts

## Motivation
All 4 control-viz calls in dev failed on 2026-04-02. Models returned text instead of images despite `responseModalities: ['IMAGE']` (3/4 calls) — the error was not classified as recoverable, so the fallback chain short-circuited without trying alternate models. The 55s timeout was also too short for preview models using thinking budgets (1337-3367 thinking tokens observed).

## What changed
Created `IMAGE_REFUSAL` error classification so response failures (no candidates, no parts, empty image data, text-only) are recoverable and the fallback chain continues. Extended `buildExhaustiveControlVizTiers()` to try all available models across both Vertex AI and AI Studio before giving up. Doubled preview timeout from 55s to 110s with 3-minute hard cap.

## Why this approach
- `IMAGE_REFUSAL` as recoverable error makes fallback chain exhaustive — one model refusing doesn't doom the entire request.
- Logging refusal text captures model reasoning for post-mortem.
- Computing chain timeout from tier count prevents runaway waits.
- Deleting legacy fallback helpers forces all code to use exhaustive chain.

## Lessons
- LLM response validation failures (empty, wrong format, refusal) should be recoverable errors so fallback chains can try alternate models — don't treat them as fatal. Created `IMAGE_REFUSAL_ERROR_CODE` in `packages/ai-orchestration/src/mastra/features/shared/vertex-error-classification.ts`.
- Preview/reasoning models need 2-3x base timeouts — thinking tokens consume time before generation starts. Changed `DEFAULT_PREVIEW_TIMEOUT_MS` from 55000 to 110000.
- Log LLM refusal text for post-mortem — refusals often have structured explanations. Extract `candidate.content.parts.filter(p => p.text)` and truncate to 500 chars.
- When quota/rate-limits are per-model-per-API, fallback chain must cross-product all models x all APIs before giving up.

## If you're working on something similar
- Classify empty/wrong-format LLM responses as recoverable errors — check `packages/ai-orchestration/src/mastra/features/shared/vertex-error-classification.ts` for the pattern.
- Use `buildExhaustiveControlVizTiers()` from `packages/ai-orchestration/src/mastra/features/hazard-control/workflows/control-viz-utils.ts` instead of manual tier lists.
- Set preview model timeouts to 2-3x base model timeouts.
- Run `rg 'throw.*Error.*No.*response'` to find validation code that should throw recoverable errors instead of generic Error.
