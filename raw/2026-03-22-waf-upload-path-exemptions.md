---
project: field1st
repo: rtslabs/field1st
pr: 297
branch: feature/waf-upload-path-exemptions
date: 2026-03-22
author: leo.brito
packages: [infra]
tags: [infra, waf, security]
related: [2026-04-07-waf-genericlfi-body-cloudfront-exemption]
answers: ["AWS WAF blocking legitimate PUT /api/documents with 9KB body", "SizeRestrictions_BODY blocking requests over 8KB", "CrossSiteScripting_BODY false positive on JPEG PNG binary data"]
---

# WAF exemptions for file upload and large-body endpoints

## Motivation
AWS WAF's `AWSManagedRulesCommonRuleSet` was blocking legitimate production traffic on dev across three services. `SizeRestrictions_BODY` blocks bodies over 8KB, affecting document saves. `CrossSiteScripting_BODY` false-positives on binary image data. Confirmed via `aws wafv2 get-sampled-requests` against live dev WAFs.

## What changed
Set `SizeRestrictions_BODY` to COUNT globally. Override `CrossSiteScripting_BODY` to COUNT in the managed rule group, then added custom re-block rules that fire when the XSS label is present AND the path is NOT a known binary upload endpoint.

## Why this approach
- `SizeRestrictions_BODY` at 8KB is too low for legitimate JSON endpoints. Rate limiting already caps abuse per IP.
- Count-then-reblock pattern is precise: override to COUNT (labels still applied), then custom rules conditionally re-block based on label + path.
- XSS body scanning stays enforced on all JSON endpoints.

## Lessons
- Managed rule label keys use title-case: `SizeRestrictions_Body` and `CrossSiteScripting_Body` (not snake_case). Confirmed via `aws wafv2 get-sampled-requests`.
- Path matching needs transformation guards: use `URL_DECODE` + `LOWERCASE` with `STARTS_WITH` to prevent encoded traversal bypasses.
- Binary upload paths are stable and identifiable by scanning routes for multipart uploads, base64 images, or raw byte proxying.

## If you're working on something similar
- Check `waf.tf` in `app_tenant/domain/`, `app_tenant/api_service/`, and `optional_modules/ai_orchestration_service/` for the three WAF configs.
- When adding a new file upload endpoint, add its path prefix to the XSS-exempt path list in the relevant WAF.
- Use AWS WAF label matching: managed rules apply labels even when overridden to COUNT. Custom rules match on labels + conditions.
- Verify with `aws wafv2 get-sampled-requests` against the live environment after applying.
