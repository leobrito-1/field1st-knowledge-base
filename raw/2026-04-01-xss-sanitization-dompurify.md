---
project: field1st
repo: rtslabs/field1st
jira: F1-187
pr: 271
branch: worktree-feature/security-sanitize-dangerouslysetinnerhtml
date: 2026-04-01
author: james.burns
packages: [web, service]
tags: [security, web, spring-boot, testing]
related: [2026-03-18-jwt-url-token-removal]
answers: ["Stored XSS via dangerouslySetInnerHTML", "User content not sanitized", "Defense description XSS", "OE description XSS", "img onerror executing JavaScript"]
files: ["packages/web/packages/field-first/src/components/Document/Defenses/DefenseDetails.tsx", "packages/web/packages/field-first/src/components/Document/OperationalExperiences/components/OECard.tsx", "packages/web/packages/field-first/src/components/clientAdmin/documents/drawer/ResponseList.tsx", "packages/web/packages/shared/src/components/Document/DocumentForm/Content.tsx", "packages/web/packages/shared/src/components/Document/DocumentForm/DrawingField.tsx"]
---

# Stored XSS prevention with three-level DOMPurify sanitization

## The problem
All uses of dangerouslySetInnerHTML passed raw unsanitized HTML to the browser. An attacker could store XSS payloads in defense descriptions or OE fields that execute in every victim's browser. HIGH-04 from the 2026 security audit.

## What we did
Integrated DOMPurify with three sanitization levels: createMarkup() for admin content, createMarkupStrict() for user-generated content, createMarkupTextOnly() for maximum security. Updated 10 components. Added 231 lines of tests covering 11 XSS attack vectors.

## Why this way and not another
- Three-level approach balances security with functionality — admin templates need more HTML than user content.
- createMarkupStrict removes links, images, and headings but preserves formatting.
- Centralized sanitizers replace per-component local helpers that had zero protection.

## What we learned
- Every dangerouslySetInnerHTML call had raw HTML with zero sanitization — trivial stored XSS. If you see dangerouslySetInnerHTML={{ __html: x }} with no sanitizer, it's a vulnerability.
- Some components had local createMarkup functions that just returned { __html: x }. Inline HTML helpers hide vulnerabilities — centralize sanitization.
- Trust boundaries matter. Audit every call site to classify as admin-controlled vs user-generated before choosing sanitization level.

## Technical reference
- Audit every dangerouslySetInnerHTML call — no sanitizer means vulnerability.
- Classify content by trust level before choosing sanitization strictness.
- Write XSS tests for every attack vector (script tags, event handlers, javascript: URLs, SVG payloads).
- Never accept JWT tokens from URL parameters — headers only.
