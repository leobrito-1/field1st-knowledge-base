---
project: field1st
repo: rtslabs/field1st
pr: 387
branch: feature/geo-allow-ph-rts-prod
date: 2026-04-02
author: leo.brito
packages: [infra]
tags: [infra, cloudfront, security]
related: []
answers: ["CloudFront blocked pentester from Philippines", "rts.field1st.com returns 403 from outside US", "How to allow specific country through CloudFront geo-restriction"]
files: ["packages/infra/terraform/live/ff-prod/tenants/rts.prod/terragrunt.hcl"]
---

# Allow Philippines access to rts.prod CloudFront

## The problem
A pentester based in the Philippines could not reach `rts.field1st.com` because all CloudFront distributions enforce US-only geo-restriction by default.

## What we did
Added `extra_country_codes = ["PH"]` to `packages/infra/terraform/live/ff-prod/tenants/rts.prod/terragrunt.hcl`, changing the CloudFront geo-restriction from `["US"]` to `["PH", "US"]` for rts.prod only.

## Why this way and not another
- Uses existing `extra_country_codes` variable — no module changes required.
- Scoped to single tenant — all other prod tenants remain US-only.

## What we learned
- CloudFront geo-restrictions apply at the distribution level, not the WAF. The `extra_country_codes` variable already existed in the Terraform module — check module inputs before writing new ones.
- Applied via `terragrunt apply -target=module.domain` to avoid full tenant rebuild.

## Technical reference
- Find the tenant's `terragrunt.hcl` in `packages/infra/terraform/live/<environment>/tenants/<tenant>/`.
- Add `extra_country_codes = ["<ISO-3166-1 alpha-2 code>"]` to the `inputs` block.
- Run `terragrunt apply -target=module.domain` from the tenant directory.
- Rollback: remove the line and re-apply.
