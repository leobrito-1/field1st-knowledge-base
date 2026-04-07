# Graph Report - /Users/leonardobrito/.claude/wiki/raw  (2026-04-07)

## Corpus Check
- Corpus is ~12,621 words - fits in a single context window. You may not need a graph.

## Summary
- 65 nodes · 127 edges · 10 communities detected
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 17 edges (avg confidence: 0.83)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `Offline Hazard Assessment` - 6 edges
2. `AI Studio Image Transport` - 5 edges
3. `WAF Upload Path Exemptions` - 5 edges
4. `Bedrock Converse Unification` - 5 edges
5. `WAF GenericLFI_BODY CloudFront Exemption` - 5 edges
6. `Web Saved Transcripts Shared Queue` - 5 edges
7. `Chat V2 Groundedness Eval` - 4 edges
8. `Java Langfuse Observability` - 4 edges
9. `Consolidate AI Orch Shared Modules` - 4 edges
10. `Consolidate Hazard Types fe-common` - 4 edges

## Surprising Connections (you probably didn't know these)
- `Chat V2 Groundedness Eval` --same_subsystem--> `Java Langfuse Observability`  [INFERRED]
  2026-03-02-chatv2-groundedness-eval.md → 2026-03-12-java-langfuse-observability.md
- `Consolidate AI Orch Shared Modules` --same_subsystem--> `Declarative Config Deep Health`  [INFERRED]
  2026-04-03-consolidate-ai-orch-shared-modules.md → 2026-03-11-declarative-config-deep-health.md
- `Consolidate AI Orch Shared Modules` --same_subsystem--> `AI Studio Image Transport`  [INFERRED]
  2026-04-03-consolidate-ai-orch-shared-modules.md → 2026-03-16-ai-studio-image-transport.md
- `BBox yxyx Standardization` --related--> `Bedrock Converse Unification`  [EXTRACTED]
  2026-03-19-bbox-yxyx-standardization.md → 2026-03-23-bedrock-converse-unification.md
- `Bedrock Converse Unification` --related--> `Hazard Eval Compression Fix`  [EXTRACTED]
  2026-03-23-bedrock-converse-unification.md → 2026-03-23-hazard-eval-compression.md

## Hyperedges (group relationships)
- **Mobile Offline Sync Ecosystem** — voice1st_offline, vlm_offline_scan, offline_hazard_assessment, offline_doc_from_hazard, offline_notifications, airplane_mode_detection, airplane_mode_recovery, sync_review_banner, per_doc_conflict, web_transcripts_queue [INFERRED]
- **WAF Security Chain** — enable_waf_prod, waf_upload_exemptions, waf_lfi_body, allow_philippines [INFERRED]
- **Multi-Provider Image Fallback** — ai_studio_image, control_viz_fallback, gpt_image_fallback, vertex_server_fetch, pdf_vertex_creds [INFERRED]
- **Bedrock Hazard Analysis Evolution** — bbox_yxyx, bedrock_converse, hazard_eval_compression, hazard_eval_retry, restore_gemini [INFERRED]
- **2026 Security Audit Remediation** — enable_waf_prod, jwt_url_removal, http_security_headers, xss_sanitization, consolidate_shared, waf_upload_exemptions, waf_lfi_body [INFERRED]

## Communities

### Community 0 - "cli"
Cohesion: 0.21
Nodes (16): Allow Philippines CloudFront, Binary Data WAF False Positive, CI Deploy Consolidation, cli, Enable WAF Production, HTTP Security Headers, infra, JWT URL Token Removal (+8 more)

### Community 1 - "mobile"
Cohesion: 0.33
Nodes (11): Airplane Mode Detection, Airplane Mode Recovery, Android Ready1st Widget, Expo Web Playwright, mobile, Offline Doc from Hazard, Offline Notifications Cache, Offline Sync Pattern (+3 more)

### Community 2 - "fe-common"
Cohesion: 0.33
Nodes (10): Cross-Platform Extraction to fe-common, fe-common, Field1st Monorepo, Form Builder Dataset Options, Hazard Side Drawer, Consolidate Hazard Types fe-common, Sentry Tracking Web Mobile, web (+2 more)

### Community 3 - "ai-orchestration"
Cohesion: 0.32
Nodes (8): ai-orchestration, AI Studio Image Transport, Bootstrap Migration Managed DB, Consolidate AI Orch Shared Modules, Declarative Config Deep Health, Eval DEMO Double Count Fix, Guardrails Allow Hazard Queries, Restore Gemini AI Settings

### Community 4 - "Async Fail-Open Observability"
Cohesion: 0.83
Nodes (4): Async Fail-Open Observability, Chat V2 Groundedness Eval, Java Langfuse Observability, Langfuse Observability

### Community 5 - "Fallback Chain Pattern"
Cohesion: 0.67
Nodes (4): Control Viz Fallback Robustness, Fallback Chain Pattern, GPT-image-1 Fallback Control Viz, Hazard Eval Model Upgrade Retry

### Community 6 - "Offline Hazard Assessment"
Cohesion: 0.67
Nodes (3): Conflict Detection Pattern, Offline Hazard Assessment, Per-Document Conflict Detection

### Community 7 - "RN 0.81 / Expo 54 Upgrade"
Cohesion: 1.0
Nodes (3): React Native Upgrade Path, RN 0.81 / Expo 54 Upgrade, RN 0.83 / Expo 55 New Arch

### Community 8 - "Image Transport (gs:// vs inlineData vs signed URLs)"
Cohesion: 0.67
Nodes (3): Image Transport (gs:// vs inlineData vs signed URLs), PDF Extraction Vertex Credentials, Vertex Server-Side Image Fetch

### Community 9 - "Bedrock Converse Unification"
Cohesion: 0.67
Nodes (3): BBox yxyx Standardization, Bedrock Converse Unification, Hazard Eval Compression Fix

## Knowledge Gaps
- **11 isolated node(s):** `Guardrails Allow Hazard Queries`, `Bootstrap Migration Managed DB`, `Restore Gemini AI Settings`, `GitHub Runner Auto-Cleanup`, `RTS Prod Tenant Setup` (+6 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `HTTP Security Headers` connect `cli` to `ai-orchestration`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Why does `Offline Hazard Assessment` connect `Offline Hazard Assessment` to `mobile`, `fe-common`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `AI Studio Image Transport` connect `ai-orchestration` to `Image Transport (gs:// vs inlineData vs signed URLs)`, `cli`, `Fallback Chain Pattern`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Offline Sync Pattern` (e.g. with `Airplane Mode Detection` and `Web Saved Transcripts Shared Queue`) actually correct?**
  _`Offline Sync Pattern` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Guardrails Allow Hazard Queries`, `Bootstrap Migration Managed DB`, `Restore Gemini AI Settings` to the rest of the system?**
  _11 weakly-connected nodes found - possible documentation gaps or missing edges._