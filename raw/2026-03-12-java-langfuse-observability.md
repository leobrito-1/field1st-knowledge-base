---
project: field1st
repo: rtslabs/field1st
pr: 211
branch: feat/java-add-langfuse-and-hallucination-observability
date: 2026-03-12
author: thomas.alfonso
packages: [service]
tags: [spring-boot, testing, typescript]
related: []
answers: ["Voice1st AI call returns finishReason=stop with no tool call", "Langfuse trace failing breaks Voice1st flow", "Pulse1st emits duplicate chat_eval_status scores", "Java AI flows have no observability for input/output/quality"]
---

# Add Langfuse observability for Java AI flows

## Motivation
Voice1st and Pulse1st AI flows had no production visibility into inputs, outputs, errors, or quality risk. We needed observability without adding latency or introducing runtime fragility.

## What changed
Added Langfuse Java client to `base-lib` with async groundedness/hallucination scoring for Voice1st and Pulse1st. Instrumented `DocumentAIService` and `Pulse1stReportProcessingService` with trace/event capture. Forced Voice1st tool call with safe fallback for empty-schema edge cases.

## Why this approach
- Async fail-open: observability calls happen in background with `@Async`. If Langfuse or eval fails, core AI flows continue.
- Forced tool call: Voice1st was hitting `finishReason=stop` with no tool call when schema was empty. Now forces tool call mode and falls back to JSON parsing if that fails.
- Groundedness eval: async judge model scores evidence support and hallucination risk.

## Lessons
- Voice1st tool call edge case: empty schema led to `finishReason=stop` hard-fail. Force tool call + safe fallback avoids this.
- Pulse1st had duplicate `chat_eval_status` in fallback path (both `n/a` and `scored`). Fixed by only emitting final status.
- Java async tracing requires careful try-catch to avoid blocking on telemetry failure.

## If you're working on something similar
- Set `application.langfuse.enabled=true` and provide `publicKey`, `secretKey`, `baseUrl`, `environment` in YAML or SSM.
- Use `AiTraceContext` builder to pass trace metadata.
- Call `chatCompletion(params, traceContext)` to capture success/error automatically.
- Groundedness eval runs async after AI call completes — configure via `application.langfuse.groundedness*` properties.
