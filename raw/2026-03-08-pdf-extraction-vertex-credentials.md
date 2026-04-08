---
project: field1st
repo: rtslabs/field1st
pr: 193
branch: fix/pdf-extraction-vertex-credentials
date: 2026-03-08
author: thomas.alfonso
packages: [ai-orchestration]
tags: [typescript, infra]
related: []
answers: ["Could not load the default credentials in PDF extraction", "PDF extraction Vertex client created before ensureGoogleCredsFile runs", "Vercel AI SDK vs Google GenAI SDK for Vertex"]
files: ["packages/ai-orchestration/src/mastra/features/ingest/lib/pdf-extraction.ts"]
---

# Fix PDF extraction Vertex credentials by switching SDKs

## Motivation
PDF extraction was failing with "Could not load the default credentials" in deployed environments. The Vercel AI SDK (`@ai-sdk/google-vertex`) created the Vertex client at module import time — before `ensureGoogleCredsFile()` had materialized the credentials file.

## What changed
Switched PDF extraction from Vercel AI SDK to Google GenAI SDK (`createInstrumentedVertexClient` + `generateContent`), the same pattern every other Vertex-dependent feature uses.

## Why this approach
- Google GenAI SDK gives explicit control over when clients are created, ensuring credentials exist first.
- Requires manual JSON schema mirroring (Vercel auto-converted Zod), explicit system instruction config, and manual response parsing.
- Image parts need explicit `inlineData` with separated mime type (handles both raw base64 and data URI formats).

## Lessons
- Module import time matters for credential-dependent SDKs. If a library creates clients at import, they miss runtime credential materialization.
- Vercel AI SDK is convenient but opaque about when clients are created. Google GenAI SDK gives explicit control.
- Image conversion from `type: 'image'` to `inlineData` requires handling both `data:image/png;base64,<data>` and raw base64 formats.

## If you're working on something similar
- Use `createInstrumentedVertexClient` for all Vertex AI calls, never `@ai-sdk/google-vertex`.
- Call `ensureGoogleCredsFile()` before creating any Vertex client.
- For JSON schema output with `generateContent`, set `config.responseMimeType: 'application/json'` and `config.responseJsonSchema`.
- Handle image parts: extract mime type from data URI prefix, separate base64 payload.
