---
project: field1st
repo: rtslabs/field1st
pr: 278
branch: feature/ai-orch-bbox-yxyx-standardization
date: 2026-03-19
author: leo.brito
packages: [ai-orchestration]
tags: [typescript]
related: [2026-03-23-bedrock-converse-unification]
answers: ["Gemini returning identical bounding boxes for all 10 hazards", "Gemini hazards all titled Trip Hazard Tools Debris with duplicate boxes", "Gemini bounding box quality degraded after prompt change"]
files: ["packages/ai-orchestration/src/mastra/features/hazard/schemas/hazard-base.ts", "packages/ai-orchestration/src/mastra/features/hazard/workflows/hazard-image-bedrock-workflow.ts", "packages/ai-orchestration/src/mastra/features/hazard/workflows/hazard-image-gemini-workflow.ts", "packages/ai-orchestration/src/mastra/features/hazard/workflows/hazard-image-openai-workflow.ts", "packages/ai-orchestration/src/mastra/features/hazard/workflows/workflow-utils.ts"]
---

# Standardize bounding box coordinates to yxyx format

## Motivation
After standardizing the shared hazard prompt to include explicit yxyx coordinate format instructions, Gemini's bounding box detection quality degraded severely. Vault1 returned all 10 hazards with identical bounding boxes. Claude and Nova followed the yxyx prompt correctly, but Gemini's native vision capability always returns yxyx regardless of prompt instructions.

## What changed
Split the shared hazard prompt into universal detection lines, explicit coordinate format lines (for Bedrock/OpenAI), and neutral format lines (for Gemini). Parameterized `buildPrompt()` with `includeCoordinateFormat` flag. Gemini passes `false`, Bedrock/OpenAI pass `true`.

## Why this approach
- Gemini's bounding box detection is native — it always returns yxyx regardless of prompt text. Adding explicit axis labels confused the model.
- Claude and OpenAI need explicit instructions — without yxyx guidance, they default to xyxy or vary across requests.
- Prompt splitting lets each provider receive optimal guidance without affecting others.

## Lessons
- Provider-native vision capabilities don't always follow prompt instructions. Gemini's bounding box format is hardwired to yxyx. Adding conflicting prompt text degraded quality rather than changing behavior.
- Validation showed the issue clearly: Gemini went from 10 identical boxes to 9 diverse hazards after removing explicit coordinate instructions.
- When standardizing prompts across multiple providers, test each provider independently with diverse inputs before applying globally.

## If you're working on something similar
- Check `packages/ai-orchestration/src/mastra/features/hazard/workflows/workflow-utils.ts` for the prompt builder with `includeCoordinateFormat` parameter.
- Gemini workflow: `buildPrompt(sceneHint, { includeCoordinateFormat: false })`.
- Bedrock/OpenAI workflows: `buildPrompt(sceneHint, { includeCoordinateFormat: true })`.
- Run eval tests with `npm run test:llm` to validate bounding box quality across all models.
