---
project: field1st
repo: rtslabs/field1st
pr: 248
branch: codex/ai-studio-hazard-image-transport
date: 2026-03-16
author: leo.brito
packages: [ai-orchestration]
tags: [typescript, security]
related: []
answers: ["AI Studio returns 400 INVALID_ARGUMENT after Vertex quota failure", "hazard image analysis fails with INVALID_ARGUMENT on AI Studio fallback", "AI Studio rejects gs:// media input"]
---

# Tier-aware image transport for Gemini hazard fallback chain

## Motivation
The hazard image analysis fallback chain reused Vertex-style `gs://` file URIs across all Gemini tiers. When a request fell through to AI Studio after Vertex quota failures, AI Studio rejected the `gs://` input with `400 INVALID_ARGUMENT`. AI Studio requires base64 `inlineData` or public HTTPS URLs — it cannot access `gs://` URIs.

## What changed
Pass `storageReadableUrl` through the hazard image route. Build Gemini image parts per fallback tier: keep `gs://` fileData for Vertex tiers and fetch the image from `storageReadableUrl` to build `inlineData` for AI Studio tiers. Added `isSafePublicHttpsImageUrl()` validation to block SSRF.

## Why this approach
- AI Studio requires base64 `inlineData` or public HTTPS URLs; it cannot access `gs://` URIs.
- Vertex tiers can use `gs://` URIs directly without fetching, reducing latency.
- Narrowing the fallback condition to `INVALID_ARGUMENT` prevents unrelated 400 errors from triggering tier downgrades.

## Lessons
- `buildGeminiPartsForCall()` in the hazard-image-gemini-workflow now checks `callConfig.aiStudio` to determine transport method. Vertex gets `fileData`, AI Studio gets `inlineData` after fetching from `storageReadableUrl`.
- Added `isSafePublicHttpsImageUrl()` in `packages/ai-orchestration/src/mastra/features/shared/safe-public-image-url.ts` to block private IP ranges, metadata endpoints, and non-HTTPS URLs. Always validate external URLs before fetching to prevent SSRF.
- The Vertex SDK surfaces errors inconsistently (numeric status vs string code). Check status, code, and message fields when classifying errors.

## If you're working on something similar
- If adding a new Gemini fallback tier, check whether it needs `gs://` URIs or `inlineData`. Update `buildGeminiPartsForCall()` accordingly.
- Always validate external image URLs before fetching. Use `assertSafePublicHttpsImageUrl()`.
- When deciding whether to continue the fallback chain after an error, check for specific error codes rather than falling back on all errors.
