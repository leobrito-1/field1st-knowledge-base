---
project: field1st
repo: rtslabs/field1st
pr: 269
branch: worktree-high-01-jwt-url
date: 2026-03-18
author: james.burns
packages: [service]
tags: [security, spring-boot]
related: [2026-04-01-xss-sanitization-dompurify]
answers: ["JWT token in URL parameters", "Token in server access logs", "Token in browser history", "Token exposed in referrer header"]
files: ["packages/service/base-lib/src/main/java/io/powerfields/forms/config/BaseSecurityConfiguration.java", "packages/service/base-lib/src/main/java/io/powerfields/forms/security/jwt/JWTFilter.java"]
---

# Restrict JWT token resolution to headers only

## The problem
JWT tokens were accepted via URL query parameters, exposing them in server access logs, browser history, referrer headers, and bookmarks. HIGH-01 from the security audit. The original intent was OAuth flow support but the implementation allowed URL tokens on all endpoints.

## What we did
Modified JWTFilter.resolveToken() to return null instead of reading URL parameters. Added SAML callback endpoint to public whitelist. Added 52 lines of tests proving URL token auth fails and header-based auth succeeds.

## Why this way and not another
- SAML callback already accepts tokens via @RequestParam in the controller — doesn't rely on JWTFilter.
- Whitelisting the SAML endpoint lets the callback bypass JWTFilter entirely.

## What we learned
- OAuth flow needed URL token acceptance, but implementation allowed it globally. When adding auth bypass for a specific flow, scope it to that endpoint only.
- URL parameters appear in server logs, browser history, referrer headers. Secrets in query strings leak everywhere.

## Technical reference
- Grep for request.getParameter in auth code — if it reads tokens, remove it.
- Add SAML/OAuth callback endpoints to the public whitelist explicitly.
- Write tests proving URL token auth fails and header-based auth succeeds.
