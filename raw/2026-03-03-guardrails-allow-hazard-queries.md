---
project: field1st
repo: rtslabs/field1st
pr: 150
branch: fix/guardrails-allow-hazard-risk-queries
date: 2026-03-03
author: thomas.alfonso
packages: [ai-orchestration]
tags: [typescript, security]
related: []
answers: ["Guardrails blocking legitimate hazard assessment questions", "Chat guardrails overly strict on safety scenario analysis", "Guardrails blocking what is the hazard of X questions"]
files: ["packages/ai-orchestration/src/mastra/features/chatv2/guardrails/guardrails-agent.ts"]
---

# Allow hazard/risk scenario questions in Chat V2 guardrails

## Motivation
Users were asking legitimate safety analysis questions ("What is the hazard of confined space entry?") and the guardrails were blocking them. The system was over-indexed on danger keywords and not distinguishing between defensive safety analysis and requests for wrongdoing.

## What changed
Updated guardrails agent prompt to explicitly allow hazard/risk assessment questions, even when hypothetical or scenario-based, unless they also contain explicit wrongdoing or policy bypass intent. Added decision priority rules.

## Why this approach
- Decision priority: first check if message is about identifying/assessing/preventing hazard/risk. If yes, allow unless requesting wrongdoing.
- Changed from "if uncertain, block" to "if uncertain and safety-related, allow."
- Danger words (confined space, fire, explosion) are expected in legitimate safety work — they don't mean block.

## Lessons
- Guardrails that over-index on keywords create false positives when the domain itself involves hazards.
- Safety/risk analysis is defensive by nature — blocking it undermines the product's core value.
- Decision priority is key: check intent first (assess vs exploit), then context, then block only on wrongdoing.

## If you're working on something similar
- Explicitly enumerate allowed intents in the guardrails prompt: "identify, assess, compare, explain, prevent, reduce."
- Add decision priority rubric so the model evaluates in order.
- Only block on explicit wrongdoing — not on domain-specific danger words.
- Remove "block when uncertain" for in-domain queries.
