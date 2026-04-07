# Graph Report - /Users/leonardobrito/.claude/wiki/raw  (2026-04-07)

## Corpus Check
- Corpus is ~5,544 words - fits in a single context window. You may not need a graph.

## Summary
- 23 nodes · 17 edges · 11 communities detected
- Extraction: 65% EXTRACTED · 35% INFERRED · 0% AMBIGUOUS · INFERRED: 6 edges (avg confidence: 0.81)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `Control Visualization Fallback on Image Refusal` - 3 edges
2. `GPT Image Fallback for Control Visualization` - 3 edges
3. `Vertex Server-Side Image Fetch` - 3 edges
4. `WAF Configuration` - 3 edges
5. `AI Studio Image Transport` - 2 edges
6. `WAF Upload Path Exemptions` - 2 edges
7. `Hazard Evaluation Compression` - 2 edges
8. `Hazard Evaluation Model Upgrade and Retry Logic` - 2 edges
9. `WAF GenericLFI_BODY CloudFront Exemption` - 2 edges
10. `Gemini Model Configuration` - 2 edges

## Surprising Connections (you probably didn't know these)
- `AI Studio Image Transport` --semantically_similar_to--> `Vertex Server-Side Image Fetch`  [INFERRED] [semantically similar]
  .claude/wiki/raw/2026-03-16-ai-studio-image-transport.md → .claude/wiki/raw/2026-04-06-vertex-server-side-image-fetch.md
- `WAF Upload Path Exemptions` --semantically_similar_to--> `WAF GenericLFI_BODY CloudFront Exemption`  [INFERRED] [semantically similar]
  .claude/wiki/raw/2026-03-22-waf-upload-path-exemptions.md → .claude/wiki/raw/2026-04-07-waf-genericlfi-body-cloudfront-exemption.md
- `Control Visualization Fallback on Image Refusal` --semantically_similar_to--> `GPT Image Fallback for Control Visualization`  [INFERRED] [semantically similar]
  .claude/wiki/raw/2026-04-02-control-viz-fallback-image-refusal.md → .claude/wiki/raw/2026-04-02-gpt-image-fallback-control-viz.md
- `Hazard Evaluation Compression` --conceptually_related_to--> `Hazard Evaluation Model Upgrade and Retry Logic`  [INFERRED]
  .claude/wiki/raw/2026-03-23-hazard-eval-compression.md → .claude/wiki/raw/2026-03-24-hazard-eval-model-upgrade-retry.md
- `Allow Philippines in CloudFront` --references--> `WAF Configuration`  [INFERRED]
  .claude/wiki/raw/2026-04-02-allow-philippines-cloudfront.md → .claude/wiki/raw/2026-03-22-waf-upload-path-exemptions.md

## Hyperedges (group relationships)
- **WAF Security Configuration Pattern** — waf_upload_path_exemptions, waf_genericlfi_body_cloudfront_exemption, waf_configuration [EXTRACTED 1.00]
- **Hazard Evaluation Pipeline** — hazard_eval_compression, hazard_eval_model_upgrade_retry, hazard_evaluation_system [EXTRACTED 1.00]
- **Image Fallback Strategy** — control_viz_fallback_image_refusal, gpt_image_fallback_control_viz, image_refusal_handling [EXTRACTED 1.00]

## Communities

### Community 0 - "AI Image Transport"
Cohesion: 0.5
Nodes (5): AI Image Transport Mechanism, AI Studio Image Transport, Gemini Model Configuration, Restore Gemini AI Settings, Vertex Server-Side Image Fetch

### Community 1 - "WAF Security"
Cohesion: 0.67
Nodes (4): Allow Philippines in CloudFront, WAF Configuration, WAF GenericLFI_BODY CloudFront Exemption, WAF Upload Path Exemptions

### Community 2 - "Control Visualization"
Cohesion: 0.83
Nodes (4): Control Visualization, Control Visualization Fallback on Image Refusal, GPT Image Fallback for Control Visualization, Image Refusal Handling Pattern

### Community 3 - "Hazard Evaluation"
Cohesion: 1.0
Nodes (3): Hazard Evaluation Compression, Hazard Evaluation Model Upgrade and Retry Logic, Hazard Evaluation System

### Community 4 - "Database Migration"
Cohesion: 1.0
Nodes (1): Bootstrap Migration to Managed DB

### Community 5 - "Config Validation"
Cohesion: 1.0
Nodes (1): Declarative Config Deep Health

### Community 6 - "Bounding Box Format"
Cohesion: 1.0
Nodes (1): BBox YXYX Standardization

### Community 7 - "Bedrock API Unification"
Cohesion: 1.0
Nodes (1): Bedrock Converse API Unification

### Community 8 - "CI/CD Runner"
Cohesion: 1.0
Nodes (1): GitHub Runner Auto Cleanup

### Community 9 - "Eval Test Isolation"
Cohesion: 1.0
Nodes (1): Evaluation Demo Double Count Fix

### Community 10 - "Shared Module Consolidation"
Cohesion: 1.0
Nodes (1): Consolidate AI Orchestration Shared Modules

## Knowledge Gaps
- **9 isolated node(s):** `Bootstrap Migration to Managed DB`, `Declarative Config Deep Health`, `Restore Gemini AI Settings`, `BBox YXYX Standardization`, `Bedrock Converse API Unification` (+4 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Database Migration`** (1 nodes): `Bootstrap Migration to Managed DB`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Config Validation`** (1 nodes): `Declarative Config Deep Health`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Bounding Box Format`** (1 nodes): `BBox YXYX Standardization`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Bedrock API Unification`** (1 nodes): `Bedrock Converse API Unification`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `CI/CD Runner`** (1 nodes): `GitHub Runner Auto Cleanup`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Eval Test Isolation`** (1 nodes): `Evaluation Demo Double Count Fix`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Shared Module Consolidation`** (1 nodes): `Consolidate AI Orchestration Shared Modules`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Are the 2 inferred relationships involving `Vertex Server-Side Image Fetch` (e.g. with `AI Studio Image Transport` and `Gemini Model Configuration`) actually correct?**
  _`Vertex Server-Side Image Fetch` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Bootstrap Migration to Managed DB`, `Declarative Config Deep Health`, `Restore Gemini AI Settings` to the rest of the system?**
  _9 weakly-connected nodes found - possible documentation gaps or missing edges._