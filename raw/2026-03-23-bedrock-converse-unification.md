---
project: field1st
repo: rtslabs/field1st
pr: 303
branch: feature/bedrock-converse-unification
date: 2026-03-23
author: leo.brito
packages: [ai-orchestration]
tags: [typescript]
related: [2026-03-23-hazard-eval-compression, 2026-03-19-bbox-yxyx-standardization]
answers: ["Nova Pro returning malformed JSON without structured output", "Two separate Bedrock code paths invokeModel and converse", "Dimension resize affecting bounding box accuracy"]
files: ["packages/ai-orchestration/src/mastra/features/ai-settings/config.ts", "packages/ai-orchestration/src/mastra/features/ai-settings/utils.ts", "packages/ai-orchestration/src/mastra/features/hazard/workflows/bedrock-model-resolution.ts", "packages/ai-orchestration/src/mastra/features/hazard/workflows/hazard-bedrock-adapters.ts", "packages/ai-orchestration/src/mastra/features/hazard/workflows/hazard-bedrock-config.ts"]
---

# Unified Bedrock hazard analysis on Converse API with Opus 4.6 and Qwen3 VL

## Motivation
Nova Pro was underperforming on dev (fewer hazards, shifted bounding boxes, malformed JSON) and the codebase had two parallel Bedrock API paths (`invokeModel` for Claude, `converse` for Nova) doing the same thing. AWS recommends Converse API for all new work.

## What changed
All Bedrock hazard analysis calls now use a single `runConverseHazardRequest()` via the Converse API. Deleted `runClaudeHazardRequest()`, `runNovaHazardRequest()`, and all Anthropic-specific response parsing. Added Opus 4.6 and Qwen3 VL. Replaced dimension resize with JPEG 75% quality compression for images over 5MB.

## Why this approach
- Single API path reduces complexity. Converse API works for all Bedrock models.
- Native structured output (`outputConfig.textFormat.json_schema`) guarantees valid JSON from Opus 4.6 and Qwen3 VL. Nova Pro doesn't support it.
- Quality compression preserves resolution. Dimension resize (max 1568px) affected bounding box accuracy. JPEG 75% compresses file size while preserving original resolution.

## Lessons
- Converse API is AWS's unified model interface. It supports all model families (Claude, Llama, Mistral, Nova) and offers native structured output via `outputConfig.textFormat.json_schema` for supported models.
- Native structured output is a major quality win. Nova Pro without structured output had frequent malformed JSON. Opus 4.6 and Qwen3 VL with `json_schema` output config never needed salvage parsing.
- Image compression should preserve resolution when accuracy matters. Resizing to max dimension 1568px was implemented to reduce file size, but for bounding box tasks, full resolution improves accuracy. JPEG quality compression achieves size reduction without losing spatial detail.

## If you're working on something similar
- Use Bedrock Converse API (`ConverseCommand`) for all new Bedrock integrations. Pass `outputConfig: { textFormat: { json: { schema: {...} } } }` for structured output.
- Check `packages/ai-orchestration/src/mastra/services/aws-bedrock.service.ts` for the Converse implementation.
- Verify model capabilities in `packages/ai-orchestration/src/mastra/features/hazard/workflows/hazard-bedrock-config.ts`.
- Test with real images across all models. Smoke test: 4 Vault images x 3 models.
