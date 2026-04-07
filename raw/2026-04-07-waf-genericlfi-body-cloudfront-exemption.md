---
project: field1st
repo: rtslabs/field1st
jira: F1-207
pr: 423
branch: feature/F1-207-waf-body-rules-count-mode
date: 2026-04-07
author: leo.brito
packages: [infra]
tags: [waf, cloudfront, infra, security]
related: []
answers: ["CloudFront returning 403 on image uploads", "GenericLFI_BODY false positive on PNG binary data", "WAF blocking document attachment uploads", "How to add a new body-rule exemption to the CloudFront WAF"]
---

# CloudFront WAF false-positive blocking PNG uploads (GenericLFI_BODY)

## Motivation
Field users upload hazard assessment photos during inspections. A PNG image was being blocked by the CloudFront WAF with a 403 error. The WAF's `GenericLFI_BODY` rule was parsing raw PNG binary as text and finding byte sequences that resemble file path traversals (`../`, `/etc/`). This is the same class of false positive as an earlier XSS fix from PR #297 — binary image data triggers text-matching rules designed for form submissions.

## What changed
Added `GenericLFI_BODY` to the existing override-to-COUNT pattern in `packages/infra/terraform/master/app_tenant/domain/waf.tf`. The reblock rule was expanded from matching only `CrossSiteScripting_Body` to matching either `CrossSiteScripting_Body` OR `GenericLFI_Body` via an `or_statement`. Upload paths (`/document-attachments/*`, `/configured-assets/*`) remain exempt; all other paths still get full body-inspection blocking. The rule was renamed from `ReblockXSSExceptUploads` to `ReblockBodyRulesExceptUploads`.

## Why this approach
- Override to COUNT + reblock on non-upload paths preserves protection everywhere except binary upload endpoints. This is the same pattern already proven for XSS false positives in PR #297.
- An `or_statement` wrapping both label matches keeps a single reblock rule instead of duplicating the path-exclusion logic.
- Renaming the rule and metric to `ReblockBodyRulesExceptUploads` makes it clear this covers multiple body-inspection rules, not just XSS.

## Lessons
- WAF sampled requests in the AWS console are the only way to identify the exact blocking rule — the 403 from CloudFront is opaque to the client. When debugging WAF 403s, always check sampled requests first.
- WAFv2 HCL does not support list-based label matching. To match multiple labels, nest individual `label_match_statement` blocks inside an `or_statement`. When adding future body-rule exemptions, add another `statement` block inside the existing `or_statement`.
- This is the second body-inspection false positive on binary data (first was XSS, now LFI). The pattern will likely recur for other rules in `AWSManagedRulesCommonRuleSet` as users upload more file types.

## If you're working on something similar
- Check WAF sampled requests in the AWS console to identify the exact rule name and label before making changes.
- The WAF override pattern lives in `packages/infra/terraform/master/app_tenant/domain/waf.tf` — search for `ReblockBodyRulesExceptUploads`.
- To add a new body-rule exemption: add a `rule_action_override` block with `count {}`, then add a `label_match_statement` inside the existing `or_statement` in the reblock rule.
- Test by uploading a large (3MB+) PNG to `/document-attachments/` on the target environment. Verify the upload succeeds AND that body-inspection rules still block on non-upload paths.
- WAF exemptions are per-WebACL. CloudFront, API Service, and AI Orchestration each have their own WAF — changes to one do not propagate to the others.
- Docker is required for Terraform apply on Apple Silicon due to `hashicorp/template` provider incompatibility.
