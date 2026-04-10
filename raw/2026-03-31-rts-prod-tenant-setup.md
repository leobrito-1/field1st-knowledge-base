---
project: field1st
repo: rtslabs/field1st
pr: 377
branch: feature/add-rts-prod-tenant
date: 2026-03-31
author: thomas.alfonso
packages: [infra]
tags: [infra, cloudfront, security]
related: []
answers: ["ssh tunnel timing out during database creation", "macOS incompatible with hashicorp/template provider", "make-secrets.sh requires hardcoded source prefix", "create-database.sh ssh tunnel only sleeps 10s before disconnecting"]
files: [".github/workflows/deploy-prod.yml", "packages/infra/scripts/create-database.sh", "packages/infra/scripts/make-secrets.sh", "packages/infra/terraform/live/ff-prod/tenants/rts.prod/ai-orchestration/terragrunt.hcl", "packages/infra/terraform/live/ff-prod/tenants/rts.prod/db/terragrunt.hcl"]
---

# Add RTS prod tenant as internal staging environment

## The problem
The team needed an internal pre-production staging environment in the prod AWS account to validate releases before deploying to customer tenants. This tenant mirrors production at smaller scale.

## What we did
Added full tenant config (`rts.prod`) in `ff-prod` with ECS cluster, Aurora DB, main app, and AI orchestration. Fixed infra scripts to support non-default keystore sources and extended SSH tunnel timeouts. Added Docker tooling for running Terraform 1.0.2 on macOS.

## Why this way and not another
- Docker for local Terraform: Apple Silicon is incompatible with `hashicorp/template` provider.
- Flexible secret source: `make-secrets.sh` now accepts optional 3rd arg for source prefix.
- SSH tunnel timeout: Increased from 10s to 120s to prevent premature disconnection during slow database creation.

## What we learned
- SSH tunnel `sleep 10` was failing mid-operation for database creation. 120s fixed the race.
- Local Terraform setup needs Docker on Apple Silicon due to template provider binary incompatibility.
- Lambda zip must be downloaded from AWS, not built locally (Go version mismatch in Dockerfile).

## Technical reference
- Use Docker image `ff-terragrunt:local` (see `packages/infra/Dockerfile.terragrunt`).
- AWS profiles need legacy SSO fields (`sso_start_url`, `sso_region`), not `sso_session`.
- Run `make-secrets.sh` with 3rd arg for custom keystore source.
- Run `create-database.sh` with patience — 120s SSH tunnel is required for slow RDS provisioning.
