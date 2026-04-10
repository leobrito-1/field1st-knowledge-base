---
project: field1st
repo: rtslabs/field1st
jira: F1-246
pr: 390
branch: feature/F1-246-gpt-image-fallback-control-viz
date: 2026-04-02
author: leo.brito
packages: [ai-orchestration]
tags: [typescript, infra]
related: [2026-04-02-control-viz-fallback-image-refusal]
answers: ["Control viz failing after all Gemini tiers exhausted", "Vertex quota errors causing control visualization 500s", "gemini-3.1-flash-image-preview not returning images"]
files: ["packages/ai-orchestration/src/mastra/features/ai-settings/config.ts", "packages/ai-orchestration/src/mastra/features/hazard-control/route/hazard-route.ts", "packages/ai-orchestration/src/mastra/features/hazard-control/workflows/control-visualization-workflow.ts", "packages/ai-orchestration/src/mastra/features/hazard-control/workflows/control-viz-openai.ts", "packages/ai-orchestration/src/mastra/features/hazard-control/workflows/control-viz-utils.ts"]
---

# Add GPT-image-1 fallback for control visualization

## The problem
When all Gemini tiers (Vertex AI + AI Studio) were exhausted due to quota or unavailability, control visualization returned user-facing 500 errors. Testing 6 image generation models showed GPT-image-1 was the only viable alternative, producing comparable quality images (~75s latency vs ~10s for Gemini, acceptable as last-resort).

## What we did
Added GPT-image-1 as terminal fallback in the control visualization chain. Decommissioned `gemini-3.1-flash-image-preview` (not returning expected results). Extended `buildExhaustiveControlVizTiers()` to accept `openAiApiKey` and append OpenAI tier when present. Updated API response to reflect the actual model that generated the image.

## Why this way and not another
- OpenAI as terminal fallback requires no new infrastructure — `OPENAI_API_KEY` already in SSM across all environments.
- `images.edit` API lets us pass the original hazard image as base, matching Gemini's in-context editing behavior.
- Returning `usedModel` in response enables monitoring which fallback tier actually succeeded.

## What we learned
- Fallback chains should support multiple providers, not just multiple models from one provider — quota limits are per-provider.
- `gemini-3.1-flash-image-preview` was returning text instead of images. Decommission broken models from catalog immediately — users will keep selecting them otherwise.
- Provider discrimination can happen at `makeCall` time — no need to fork the entire fallback chain for mixed providers.
- When fallback chains can use different models, return which one actually succeeded for monitoring and cost analysis.

## Technical reference
- Import `buildExhaustiveControlVizTiers` from `packages/ai-orchestration/src/mastra/features/hazard-control/workflows/control-viz-utils.ts`.
- Use `images.edit` API (not `images.generate`) when you have a base image to modify.
- Check `packages/ai-orchestration/src/mastra/features/hazard-control/workflows/control-viz-openai.ts` for OpenAI Langfuse span tracing pattern.
- Set timeout to 180s for GPT-image-1 calls — observed 75s median latency.
