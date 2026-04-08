---
project: field1st
repo: rtslabs/field1st
pr: 133
branch: feat/chatv2-groundedness-langfuse-metrics
date: 2026-03-02
author: thomas.alfonso
packages: [ai-orchestration]
tags: [typescript, testing]
related: []
answers: ["Chat V2 has no quality observability", "No visibility into hallucination risk in Chat V2 responses", "How to score groundedness for RAG chat answers"]
files: ["packages/ai-orchestration/src/config.ts", "packages/ai-orchestration/src/mastra/features/chatv2/observability/groundedness-evaluator.ts", "packages/ai-orchestration/src/mastra/features/chatv2/orchestrator-workflow-v2.ts", "packages/ai-orchestration/src/mastra/features/observability/langfuse-score-publisher.ts"]
---

# Add groundedness evaluation and observability for Chat V2

## Motivation
Chat V2 responses had no automated quality assessment. We needed to detect when answers were unsupported by evidence or contradicted page context, without blocking the response or adding latency.

## What changed
Added async groundedness evaluator that scores evidence support and page context alignment after each Chat V2 response. Publishes scores to Langfuse. Added config for model, timeouts, thresholds, and truncation limits.

## Why this approach
- Async non-blocking: evaluation runs after response is sent, never delays the user.
- Two-part scoring: evidence groundedness (RAG support) + page context alignment (no contradiction).
- Combined risk: weighted combination (0.7 * evidence + 0.3 * pageContext) surfaces highest-risk answers.
- Fail-open: if eval fails, publish `eval_error` status but don't break the response flow.
- Page context is sanitized (emails, phones, sensitive keys) before sending to judge model.

## Lessons
- Groundedness judge model needs explicit rubric: >=0.85 strongly supported, 0.65-0.84 mostly supported, <0.65 unsupported.
- Truncation limits are critical: 12k chars for evidence, 8k for page context prevents token overflow.
- Evidence extraction must handle multiple tool types: `search-knowledge-base` has nested structure.
- Combined risk makes triage easier: single score surfaces high hallucination probability.

## If you're working on something similar
qo- Set `CHAT_GROUNDEDNESS_EVAL_ENABLED=true`, `CHAT_GROUNDEDNESS_EVAL_MODEL=gpt-4.1-mini`, `CHAT_GROUNDEDNESS_EVAL_TIMEOUT_MS=8000`.
- Use `buildEvidenceContext(toolOutputs, maxChars)` to normalize KB and tool outputs.
- Use `sanitizePageContext(pageContext)` to redact PII before eval.
- Check `chat_hallucination_risk` score: >0.35 is alert threshold.
