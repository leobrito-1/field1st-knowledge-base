---
project: field1st
repo: rtslabs/field1st
pr: 264
branch: feature/critical-01-enable-waf-production
date: 2026-03-18
author: james.burns
packages: [infra]
tags: [infra, waf, cloudfront, security]
related: [2026-03-22-waf-upload-path-exemptions, 2026-04-07-waf-genericlfi-body-cloudfront-exemption]
answers: ["Production tenants have no WAF", "All 9 tenants exposed without WAF", "WAF not attached to CloudFront", "CloudFront distribution has empty web_acl_id", "WAF conditional logic backwards"]
files: ["packages/infra/terraform/master/app_tenant/api_service/waf.tf", "packages/infra/terraform/master/app_tenant/domain/main.tf", "packages/infra/terraform/master/app_tenant/domain/waf.tf", "packages/infra/terraform/master/optional_modules/ai_orchestration_service/waf.tf"]
---

# Enable WAF for all production services via inverted logic fix

## Motivation
All 9 production tenants were exposed without WAF protection. The Terraform conditional had backwards logic: make_public ? "" : waf_arn disabled WAF for public sites instead of enabling it. The AI orchestration service had no WAF at all. CRITICAL-01 from penetration test.

## What changed
Simplified CloudFront WAF to always-enabled (removed conditional). Deleted unused IP whitelist WAF resources (~128 lines). Enhanced API backend WAF with AWS Managed Rules. Added new WAF for AI orchestration ALB.

## Why this approach
- Conditional logic was inverted — removed the toggle entirely. WAF is always on.
- AWS Managed Rules provide OWASP Top 10 coverage without custom rule maintenance.
- Rate limiting at 2000 requests per 5 minutes per IP.
- All three layers (CloudFront, API ALB, AI orchestration ALB) now have WAF.

## Lessons
- Terraform conditional make_public ? "" : waf_arn disabled WAF for public sites. Conditional security controls are dangerous — enable unconditionally and remove the toggle.
- 128 lines of unused IP whitelist WAF resources were defined but never attached. Dead code hides real config. Delete unused resources.
- AI orchestration had zero WAF. When adding a new service, audit the security checklist. Don't assume defaults are safe.

## If you're working on something similar
- Run terragrunt plan in a pilot tenant before applying to all production tenants.
- Verify web_acl_id changes from empty to arn:aws:wafv2 in the plan.
- Monitor CloudWatch WAF metrics for false positives after deploy.
- Deploy to single tenant first, monitor 30 minutes, then roll out.
