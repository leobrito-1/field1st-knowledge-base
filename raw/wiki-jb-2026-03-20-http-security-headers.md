---
project: field1st
repo: rtslabs/field1st
jira: F1-197
pr: 286
branch: fix/security-headers
date: 2026-03-20
author: james.burns
packages: [infra, service, ai-orchestration]
tags: [infra, security, cloudfront, spring-boot]
related: []
answers: ["Missing HTTP security headers", "CloudFront CSP placeholder default-src self", "X-Frame-Options disabled with frameOptions disable", "AI orchestration has no security headers"]
files: ["packages/ai-orchestration/src/mastra/index.ts", "packages/infra/terraform/master/app_tenant/domain/main.tf", "packages/service/base-lib/src/main/java/io/powerfields/forms/config/BaseSecurityConfiguration.java"]
---

# HTTP security headers across CloudFront, Spring Boot, and AI orchestration

## Motivation
HTTP security headers were missing or misconfigured across the stack. CloudFront had a non-functional placeholder CSP. Spring Boot was actively calling frameOptions(disable). The AI orchestration service had no security headers at all.

## What changed
Added CloudFront response headers policy with X-Frame-Options (DENY), HSTS, X-Content-Type-Options, Referrer-Policy, and full CSP. Re-enabled X-Frame-Options in Spring Security. Added Hono secureHeaders() middleware to AI orchestration (CSP omitted — pure JSON API).

## Why this approach
- CloudFront response headers policy applies to all cache behaviors without modifying origin responses.
- CSP connect-src uses wildcard to cover API domains per environment.
- Spring Security matches CloudFront policy for defense-in-depth.
- SAML warning added — X-Frame-Options DENY may break IdPs using iframe POST-binding.

## Lessons
- Placeholder CSPs fail silently. Audit browser console for violations before deploying strict policies.
- When re-enabling disabled security features, document why they were disabled to prevent regressions.
- Pure JSON APIs need security headers too (X-Frame-Options, HSTS). CSP is the only one you can skip.

## If you're working on something similar
- Run curl -I before and after to verify headers appear.
- Check browser console for CSP violations after deploy.
- Test SAML login flow if enabling X-Frame-Options DENY.
- Add wss:// to CSP connect-src for WebSocket endpoints.
- HSTS preload requires includeSubDomains and 1-year max-age.
