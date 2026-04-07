# Graph Report - /Users/leonardobrito/.claude/wiki/raw  (2026-04-07)

## Corpus Check
- Corpus is ~6,688 words - fits in a single context window. You may not need a graph.

## Summary
- 28 nodes · 30 edges · 8 communities detected
- Extraction: 57% EXTRACTED · 43% INFERRED · 0% AMBIGUOUS · INFERRED: 13 edges (avg confidence: 0.77)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `Chat V2 Groundedness Eval` - 4 edges
2. `Tier-Aware Image Transport for Gemini Fallback` - 4 edges
3. `PDF Extraction Vertex Credentials Fix` - 3 edges
4. `Java Langfuse Observability` - 3 edges
5. `Bedrock Converse API Unification` - 3 edges
6. `Hazard Eval Compression and Result Accumulation Fix` - 3 edges
7. `Hazard Eval Model Upgrade and 5xx Retry` - 3 edges
8. `Consolidate AI Orchestration Shared Modules` - 3 edges
9. `Declarative Config and Deep Health Checks` - 2 edges
10. `WAF Upload Path Exemptions` - 2 edges

## Surprising Connections (you probably didn't know these)
- `Chat V2 Groundedness Eval` --conceptually_related_to--> `Java Langfuse Observability`  [INFERRED]
  /Users/leonardobrito/.claude/wiki/raw/2026-03-02-chatv2-groundedness-eval.md → /Users/leonardobrito/.claude/wiki/raw/2026-03-12-java-langfuse-observability.md
- `Guardrails Allow Hazard Queries` --conceptually_related_to--> `Chat V2 Groundedness Eval`  [INFERRED]
  /Users/leonardobrito/.claude/wiki/raw/2026-03-03-guardrails-allow-hazard-queries.md → /Users/leonardobrito/.claude/wiki/raw/2026-03-02-chatv2-groundedness-eval.md
- `Consolidate AI Orchestration Shared Modules` --conceptually_related_to--> `PDF Extraction Vertex Credentials Fix`  [INFERRED]
  /Users/leonardobrito/.claude/wiki/raw/2026-04-03-consolidate-ai-orch-shared-modules.md → /Users/leonardobrito/.claude/wiki/raw/2026-03-08-pdf-extraction-vertex-credentials.md
- `Consolidate AI Orchestration Shared Modules` --conceptually_related_to--> `Declarative Config and Deep Health Checks`  [INFERRED]
  /Users/leonardobrito/.claude/wiki/raw/2026-04-03-consolidate-ai-orch-shared-modules.md → /Users/leonardobrito/.claude/wiki/raw/2026-03-11-declarative-config-deep-health.md
- `Tier-Aware Image Transport for Gemini Fallback` --conceptually_related_to--> `Vertex Server-Side Image Fetch`  [INFERRED]
  /Users/leonardobrito/.claude/wiki/raw/2026-03-16-ai-studio-image-transport.md → /Users/leonardobrito/.claude/wiki/raw/2026-04-06-vertex-server-side-image-fetch.md

## Hyperedges (group relationships)
- **Langfuse Across Java and TypeScript** — chatv2_groundedness_eval, java_langfuse_observability, concept_langfuse_observability, concept_async_fail_open [INFERRED 0.90]
- **WAF Binary Data False Positive Series** — waf_upload_path_exemptions, waf_genericlfi_body_cloudfront_exemption, concept_binary_data_false_positive [EXTRACTED 1.00]
- **Image Transport Method Evolution** — ai_studio_image_transport, vertex_server_side_image_fetch, pdf_extraction_vertex_credentials, concept_image_transport [INFERRED 0.85]
- **Control Viz Exhaustive Fallback Chain** — control_viz_fallback_image_refusal, gpt_image_fallback_control_viz, concept_fallback_chain_pattern [EXTRACTED 1.00]
- **Hazard Eval Test Infrastructure Fixes** — hazard_eval_compression, hazard_eval_model_upgrade_retry, eval_demo_double_count [INFERRED 0.85]

## Communities

### Community 0 - "Image Transport & Credentials"
Cohesion: 0.43
Nodes (7): Tier-Aware Image Transport for Gemini Fallback, Credential Initialization Timing, Image Transport (gs:// vs inlineData vs signed URLs), Consolidate AI Orchestration Shared Modules, Declarative Config and Deep Health Checks, PDF Extraction Vertex Credentials Fix, Vertex Server-Side Image Fetch

### Community 1 - "Hazard Detection Pipeline"
Cohesion: 0.33
Nodes (6): Bounding Box yxyx Standardization, Bedrock Converse API Unification, Eval DEMO Double Count Fix, Hazard Eval Compression and Result Accumulation Fix, Hazard Eval Model Upgrade and 5xx Retry, Restore Gemini AI Settings Catalog

### Community 2 - "Observability & Chat Quality"
Cohesion: 0.6
Nodes (5): Chat V2 Groundedness Eval, Async Fail-Open Observability, Langfuse Observability, Guardrails Allow Hazard Queries, Java Langfuse Observability

### Community 3 - "WAF Security"
Cohesion: 1.0
Nodes (3): Binary Data WAF False Positive, WAF GenericLFI_BODY CloudFront Exemption, WAF Upload Path Exemptions

### Community 4 - "Control Visualization Fallback"
Cohesion: 1.0
Nodes (3): Fallback Chain Pattern, Control-Viz Fallback for Image Refusal, GPT-image-1 Fallback for Control Viz

### Community 5 - "Prod Infrastructure"
Cohesion: 1.0
Nodes (2): Allow Philippines Access to CloudFront, RTS Prod Tenant Setup

### Community 6 - "Database Migration"
Cohesion: 1.0
Nodes (1): Bootstrap Migration for Managed DB

### Community 7 - "CI/CD Runner"
Cohesion: 1.0
Nodes (1): GitHub Runner Auto-Cleanup

## Knowledge Gaps
- **8 isolated node(s):** `Guardrails Allow Hazard Queries`, `Bootstrap Migration for Managed DB`, `Restore Gemini AI Settings Catalog`, `Bounding Box yxyx Standardization`, `GitHub Runner Auto-Cleanup` (+3 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Prod Infrastructure`** (2 nodes): `Allow Philippines Access to CloudFront`, `RTS Prod Tenant Setup`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Database Migration`** (1 nodes): `Bootstrap Migration for Managed DB`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `CI/CD Runner`** (1 nodes): `GitHub Runner Auto-Cleanup`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Hazard Eval Model Upgrade and 5xx Retry` connect `Hazard Detection Pipeline` to `Observability & Chat Quality`, `Control Visualization Fallback`?**
  _High betweenness centrality (0.356) - this node is a cross-community bridge._
- **Why does `Tier-Aware Image Transport for Gemini Fallback` connect `Image Transport & Credentials` to `Control Visualization Fallback`?**
  _High betweenness centrality (0.247) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Chat V2 Groundedness Eval` (e.g. with `Java Langfuse Observability` and `Guardrails Allow Hazard Queries`) actually correct?**
  _`Chat V2 Groundedness Eval` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Tier-Aware Image Transport for Gemini Fallback` (e.g. with `Vertex Server-Side Image Fetch` and `Consolidate AI Orchestration Shared Modules`) actually correct?**
  _`Tier-Aware Image Transport for Gemini Fallback` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `PDF Extraction Vertex Credentials Fix` (e.g. with `Image Transport (gs:// vs inlineData vs signed URLs)` and `Consolidate AI Orchestration Shared Modules`) actually correct?**
  _`PDF Extraction Vertex Credentials Fix` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Guardrails Allow Hazard Queries`, `Bootstrap Migration for Managed DB`, `Restore Gemini AI Settings Catalog` to the rest of the system?**
  _8 weakly-connected nodes found - possible documentation gaps or missing edges._