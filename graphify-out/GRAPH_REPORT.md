# Graph Report - /Users/leonardobrito/.claude/wiki/raw  (2026-04-07)

## Corpus Check
- Corpus is ~6,688 words - fits in a single context window. You may not need a graph.

## Summary
- 35 nodes · 58 edges · 6 communities detected
- Extraction: 78% EXTRACTED · 22% INFERRED · 0% AMBIGUOUS · INFERRED: 13 edges (avg confidence: 0.77)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `Chat V2 Groundedness Eval` - 5 edges
2. `Tier-Aware Image Transport for Gemini Fallback` - 5 edges
3. `PDF Extraction Vertex Credentials Fix` - 4 edges
4. `Java Langfuse Observability` - 4 edges
5. `Bedrock Converse API Unification` - 4 edges
6. `Hazard Eval Compression and Result Accumulation Fix` - 4 edges
7. `Hazard Eval Model Upgrade and 5xx Retry` - 4 edges
8. `Consolidate AI Orchestration Shared Modules` - 4 edges
9. `Declarative Config and Deep Health Checks` - 3 edges
10. `WAF Upload Path Exemptions` - 3 edges

## Surprising Connections (you probably didn't know these)
- `Chat V2 Groundedness Eval` --conceptually_related_to--> `Guardrails Allow Hazard Queries`  [INFERRED]
  /Users/leonardobrito/.claude/wiki/raw/2026-03-02-chatv2-groundedness-eval.md → /Users/leonardobrito/.claude/wiki/raw/2026-03-03-guardrails-allow-hazard-queries.md
- `Chat V2 Groundedness Eval` --conceptually_related_to--> `Java Langfuse Observability`  [INFERRED]
  /Users/leonardobrito/.claude/wiki/raw/2026-03-02-chatv2-groundedness-eval.md → /Users/leonardobrito/.claude/wiki/raw/2026-03-12-java-langfuse-observability.md
- `PDF Extraction Vertex Credentials Fix` --conceptually_related_to--> `Consolidate AI Orchestration Shared Modules`  [INFERRED]
  /Users/leonardobrito/.claude/wiki/raw/2026-03-08-pdf-extraction-vertex-credentials.md → /Users/leonardobrito/.claude/wiki/raw/2026-04-03-consolidate-ai-orch-shared-modules.md
- `Declarative Config and Deep Health Checks` --conceptually_related_to--> `Consolidate AI Orchestration Shared Modules`  [INFERRED]
  /Users/leonardobrito/.claude/wiki/raw/2026-03-11-declarative-config-deep-health.md → /Users/leonardobrito/.claude/wiki/raw/2026-04-03-consolidate-ai-orch-shared-modules.md
- `Tier-Aware Image Transport for Gemini Fallback` --conceptually_related_to--> `Vertex Server-Side Image Fetch`  [INFERRED]
  /Users/leonardobrito/.claude/wiki/raw/2026-03-16-ai-studio-image-transport.md → /Users/leonardobrito/.claude/wiki/raw/2026-04-06-vertex-server-side-image-fetch.md

## Communities

### Community 0 - "ai-orchestration"
Cohesion: 0.36
Nodes (9): Bounding Box yxyx Standardization, Bedrock Converse API Unification, Bootstrap Migration for Managed DB, Eval DEMO Double Count Fix, Guardrails Allow Hazard Queries, Hazard Eval Compression and Result Accumulation Fix, Hazard Eval Model Upgrade and 5xx Retry, ai-orchestration (+1 more)

### Community 1 - "infra"
Cohesion: 0.43
Nodes (7): Allow Philippines Access to CloudFront, Binary Data WAF False Positive, GitHub Runner Auto-Cleanup, infra, RTS Prod Tenant Setup, WAF GenericLFI_BODY CloudFront Exemption, WAF Upload Path Exemptions

### Community 2 - "Image Transport & Credentials"
Cohesion: 0.43
Nodes (7): Tier-Aware Image Transport for Gemini Fallback, Credential Initialization Timing, Image Transport (gs:// vs inlineData vs signed URLs), Consolidate AI Orchestration Shared Modules, Declarative Config and Deep Health Checks, PDF Extraction Vertex Credentials Fix, Vertex Server-Side Image Fetch

### Community 3 - "Field1st Project"
Cohesion: 0.4
Nodes (5): Field1st, fe-common, mobile, service, web

### Community 4 - "Observability & Chat Quality"
Cohesion: 0.83
Nodes (4): Chat V2 Groundedness Eval, Async Fail-Open Observability, Langfuse Observability, Java Langfuse Observability

### Community 5 - "Control Visualization Fallback"
Cohesion: 1.0
Nodes (3): Fallback Chain Pattern, Control-Viz Fallback for Image Refusal, GPT-image-1 Fallback for Control Viz

## Knowledge Gaps
- **2 isolated node(s):** `Bootstrap Migration for Managed DB`, `GitHub Runner Auto-Cleanup`
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Chat V2 Groundedness Eval` connect `Observability & Chat Quality` to `ai-orchestration`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._
- **Why does `PDF Extraction Vertex Credentials Fix` connect `Image Transport & Credentials` to `ai-orchestration`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `Hazard Eval Model Upgrade and 5xx Retry` connect `ai-orchestration` to `Observability & Chat Quality`, `Control Visualization Fallback`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Chat V2 Groundedness Eval` (e.g. with `Java Langfuse Observability` and `Guardrails Allow Hazard Queries`) actually correct?**
  _`Chat V2 Groundedness Eval` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Tier-Aware Image Transport for Gemini Fallback` (e.g. with `Vertex Server-Side Image Fetch` and `Consolidate AI Orchestration Shared Modules`) actually correct?**
  _`Tier-Aware Image Transport for Gemini Fallback` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Bootstrap Migration for Managed DB`, `GitHub Runner Auto-Cleanup` to the rest of the system?**
  _2 weakly-connected nodes found - possible documentation gaps or missing edges._