# Graph Report - /Users/leonardobrito/.claude/wiki/raw  (2026-04-07)

## Corpus Check
- Corpus is ~11,738 words - fits in a single context window. You may not need a graph.

## Summary
- 60 nodes · 117 edges · 11 communities detected
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 20 edges (avg confidence: 0.77)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `Offline Hazard Assessment` - 6 edges
2. `AI Studio Image Transport` - 5 edges
3. `Bedrock Converse API Unification` - 5 edges
4. `Vertex Server-Side Image Fetch` - 5 edges
5. `Consolidate Hazard Types to fe-common` - 5 edges
6. `Chat V2 Groundedness Eval` - 4 edges
7. `Declarative Config and Deep Health Checks` - 4 edges
8. `Java Langfuse Observability` - 4 edges
9. `Hazard Eval Compression Fix` - 4 edges
10. `Consolidate AI Orch Shared Modules` - 4 edges

## Surprising Connections (you probably didn't know these)
- `Chat V2 Groundedness Eval` --semantically_similar_to--> `Java Langfuse Observability`  [INFERRED] [semantically similar]
  ~/.claude/wiki/raw/2026-03-02-chatv2-groundedness-eval.md → ~/.claude/wiki/raw/2026-03-12-java-langfuse-observability.md
- `Sentry Tracking Web and Mobile` --conceptually_related_to--> `Declarative Config and Deep Health Checks`  [INFERRED]
  ~/.claude/wiki/raw/wiki-ae-2026-04-06-sentry-tracking-web-mobile.md → ~/.claude/wiki/raw/2026-03-11-declarative-config-deep-health.md
- `Consolidate AI Orch Shared Modules` --conceptually_related_to--> `AI Studio Image Transport`  [INFERRED]
  ~/.claude/wiki/raw/2026-04-03-consolidate-ai-orch-shared-modules.md → ~/.claude/wiki/raw/2026-03-16-ai-studio-image-transport.md
- `Restore Gemini AI Settings` --conceptually_related_to--> `Bedrock Converse API Unification`  [INFERRED]
  ~/.claude/wiki/raw/2026-03-18-restore-gemini-ai-settings.md → ~/.claude/wiki/raw/2026-03-23-bedrock-converse-unification.md
- `GitHub Runner Auto-Cleanup` --conceptually_related_to--> `CI Deploy Consolidation`  [INFERRED]
  ~/.claude/wiki/raw/2026-03-25-github-runner-auto-cleanup.md → ~/.claude/wiki/raw/wiki-ae-2026-02-23-ci-deploy-consolidation.md

## Hyperedges (group relationships)
- **Mobile Offline Sync Ecosystem** — voice1st_offline_save, vlm_offline_scan, offline_hazard_assessment, offline_doc_from_hazard, offline_notifications_cache, airplane_mode_detection, airplane_mode_recovery, offline_sync_review_banner, per_document_conflict [INFERRED 0.95]
- **Hazard Analysis Multi-Provider Fallback** — ai_studio_image_transport, bedrock_converse, bbox_yxyx, hazard_eval_compression, hazard_eval_retry, restore_gemini_settings, control_viz_fallback_refusal, gpt_image_fallback [INFERRED 0.90]
- **Image Transport Format Evolution** — pdf_extraction_vertex, ai_studio_image_transport, vertex_server_side_fetch, hazard_eval_compression, consolidate_ai_orch_shared [INFERRED 0.85]
- **WAF Binary Data False Positive Series** — waf_upload_exemptions, waf_genericlfi_body [EXTRACTED 1.00]
- **Cross-Platform Code Extraction to fe-common** — consolidate_hazard_types, web_saved_transcripts, offline_hazard_assessment, hazard_side_drawer, form_builder_dataset, airplane_mode_recovery, offline_sync_review_banner [INFERRED 0.85]

## Communities

### Community 0 - "CLI Package"
Cohesion: 0.29
Nodes (10): Allow Philippines CloudFront Access, Binary Data WAF False Positive, CLI Package, Field1st Monorepo, GitHub Runner Auto-Cleanup, Infrastructure Package, Monorepo Migration, RTS Prod Tenant Setup (+2 more)

### Community 1 - "FE Common Package"
Cohesion: 0.39
Nodes (9): Consolidate Hazard Types to fe-common, Cross-Platform Extraction to fe-common, FE Common Package, Form Builder Dataset Options, Offline Hazard Assessment, Sentry Tracking Web and Mobile, Web Package, Web Reports DnD Charts (+1 more)

### Community 2 - "Service Package"
Cohesion: 0.38
Nodes (7): Async Fail-Open Observability, Chat V2 Groundedness Eval, CI Deploy Consolidation, Hazard Assessment Side Drawer, Java Langfuse Observability, Langfuse Observability, Service Package

### Community 3 - "AI Orchestration Package"
Cohesion: 0.4
Nodes (6): AI Orchestration Package, Bootstrap Migration for Managed DB, Consolidate AI Orch Shared Modules, Declarative Config and Deep Health Checks, Eval Demo Double Count Fix, Guardrails Allow Hazard Queries

### Community 4 - "Offline Sync Pattern"
Cohesion: 0.4
Nodes (6): Offline Document from Hazard, Offline Notifications Cache, Offline Sync Pattern, Offline Sync Review Banner, VLM Offline Scan, Voice1st Offline Save

### Community 5 - "Mobile Package"
Cohesion: 0.53
Nodes (6): Android Ready1st Widget, Expo Web for Playwright, Mobile Package, React Native Upgrade Pattern, RN 0.81 / Expo 54 Upgrade, RN 0.83 / Expo 55 + New Architecture

### Community 6 - "Bedrock Converse API Unification"
Cohesion: 0.4
Nodes (5): Bounding Box yxyx Standardization, Bedrock Converse API Unification, Hazard Eval Compression Fix, Hazard Eval Model Upgrade and Retry, Restore Gemini AI Settings

### Community 7 - "AI Studio Image Transport"
Cohesion: 0.83
Nodes (4): AI Studio Image Transport, Image Transport (gs:// vs inlineData vs signed URLs), PDF Extraction Vertex Credentials Fix, Vertex Server-Side Image Fetch

### Community 8 - "Fallback Chain Pattern"
Cohesion: 1.0
Nodes (3): Control Viz Fallback Image Refusal, Fallback Chain Pattern, GPT-image-1 Fallback for Control Viz

### Community 9 - "Airplane Mode Recovery"
Cohesion: 1.0
Nodes (2): Airplane Mode Detection, Airplane Mode Recovery

### Community 10 - "Per-Document Conflict Detection"
Cohesion: 1.0
Nodes (2): Conflict Detection (Per-Document Timestamp), Per-Document Conflict Detection

## Knowledge Gaps
- **5 isolated node(s):** `Guardrails Allow Hazard Queries`, `Bootstrap Migration for Managed DB`, `Eval Demo Double Count Fix`, `Web Reports DnD Charts`, `Android Ready1st Widget`
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Airplane Mode Recovery`** (2 nodes): `Airplane Mode Detection`, `Airplane Mode Recovery`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Per-Document Conflict Detection`** (2 nodes): `Conflict Detection (Per-Document Timestamp)`, `Per-Document Conflict Detection`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Offline Hazard Assessment` connect `FE Common Package` to `Per-Document Conflict Detection`, `Offline Sync Pattern`, `Mobile Package`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `Declarative Config and Deep Health Checks` connect `AI Orchestration Package` to `FE Common Package`, `Service Package`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Why does `Sentry Tracking Web and Mobile` connect `FE Common Package` to `AI Orchestration Package`, `Mobile Package`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **What connects `Guardrails Allow Hazard Queries`, `Bootstrap Migration for Managed DB`, `Eval Demo Double Count Fix` to the rest of the system?**
  _5 weakly-connected nodes found - possible documentation gaps or missing edges._