---
project: field1st
repo: rtslabs/field1st
pr: 263
branch: codex/ai-orch-bedrock-ingress-consistency
date: 2026-03-18
author: leo.brito
packages: [ai-orchestration]
tags: [typescript]
related: []
answers: ["Gemini hazard models missing from ai-settings catalog", "hazard model defaulting to Bedrock instead of Gemini", "Gemini 2.5 Flash not showing in ai-settings"]
---

# Restore Gemini hazard models to ai-settings catalog

## Motivation
After adding Bedrock hazard model support, the ai-settings catalog was inadvertently changed to expose only Bedrock models. The default hazard model was also changed from Gemini 2.5 Flash to Bedrock Opus 4.5, causing a mismatch between the intended default and what was displayed.

## What changed
Restored Gemini 2.5 Flash and Gemini 3.1 Pro to the hazard model catalog alongside the Bedrock models, and set Gemini 2.5 Flash back as the default hazard model.

## Why this approach
- Hazard analysis runs on both Gemini and Bedrock depending on quota and fallback tier.
- The ai-settings catalog should reflect all available models, not just the most recently added provider.
- Gemini 2.5 Flash is the production default for cost and latency reasons.

## Lessons
- `AVAILABLE_HAZARD_MODELS` in `packages/ai-orchestration/src/mastra/features/ai-settings/config.ts` defines the catalog and default. When adding a new provider, append to the catalog rather than replacing existing entries.

## If you're working on something similar
- When adding a new provider to the hazard model catalog, append entries to `AVAILABLE_HAZARD_MODELS` in `config.ts`.
- Verify `DEFAULT_HAZARD_MODEL` matches the production default used by routing logic.
- Run tests in `src/mastra/features/ai-settings/__tests__/` to confirm catalog consistency.
