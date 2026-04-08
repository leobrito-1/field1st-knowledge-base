---
project: field1st
repo: rtslabs/field1st
jira: F1-264
pr: 418
branch: feature/F1-264-vertex-server-side-image-fetch
date: 2026-04-06
author: leo.brito
packages: [ai-orchestration]
tags: [infra, security, typescript]
related: []
answers: ["Cannot fetch content from the provided URL", "Vertex hazard analysis failing with signed URL error", "Signed S3 URL expired before Vertex AI processed request"]
files: ["packages/ai-orchestration/src/mastra/features/hazard/workflows/hazard-image-gemini-workflow.ts", "packages/ai-orchestration/src/mastra/shared/image/fetch-image.ts"]
---

# Fetch HTTPS images server-side for Vertex hazard analysis

## Motivation
Vertex AI hazard image analysis was passing HTTPS signed URLs directly to the API as `fileData`, requiring Vertex to fetch the image remotely. When signed URLs expired between the server receiving the request and Vertex processing it, the call failed with "Cannot fetch content from the provided URL." CloudWatch logs showed 29 errors in a single day from this pattern.

## What changed
The Gemini hazard workflow now fetches HTTPS images server-side via `fetchImageAsBase64()` and passes them as `inlineData` (base64) instead of `fileData`. Added 10MB size guard and fixed timeout handling so the AbortSignal covers body download. `gs://` paths unchanged — they use IAM-based access and don't expire.

## Why this approach
- Eliminates the race condition — image is fetched once by the server with control over timeouts
- Signed URLs are consumed immediately, not passed to external services where timing is unpredictable
- 10MB guard leaves headroom under Vertex's 20MB-per-request limit
- `gs://` paths use IAM auth (no expiration) and Vertex fetches them efficiently within Google's network

## Lessons
- Signed URLs passed as `fileData` to Vertex AI expired before processing, causing 29 failures in one day. Never pass time-sensitive URLs to external APIs as fetch-on-demand resources — consume them server-side and pass the data inline.
- The original `fetchInlineDataPart()` cleared timeout in `.then()` before body download completed. Moved `clearTimeout` to `finally` block so AbortSignal covers the entire operation including `response.arrayBuffer()`.
- No size guard meant a 50MB image could be base64-encoded (67MB) and sent to Vertex. Always validate content size before base64 encoding — base64 inflates size by ~33%.

## If you're working on something similar
- Search for `fileData: { fileUri:` in workflow code — any HTTPS signed URL usage is suspect.
- Use `fetchImageAsBase64()` from `packages/ai-orchestration/src/mastra/shared/image/fetch-image.ts` for any image URL passed to external AI APIs.
- Add `maxBytes` parameter to `fetchImageAsBase64()` calls for API-specific size limits.
- When using `AbortController` with `fetch()`, ensure the signal remains active through `response.arrayBuffer()` — put cleanup in `finally`.
