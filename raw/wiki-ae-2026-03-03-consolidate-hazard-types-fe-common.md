---
project: field1st
repo: rtslabs/field1st
pr: 151
branch: feature/consolidate-hazard-types-utils
date: 2026-03-03
author: andy.ewald
packages: [fe-common, web, mobile]
tags: [fe-common, web, mobile, typescript]
related: []
answers: ["hazard types differ between web and mobile", "structureVersion hardcoded", "type drift across packages"]
files: ["packages/fe-common/src/index.ts", "packages/fe-common/src/types/hazardAnalysis.ts", "packages/fe-common/src/utils/hazard/controlUtils.ts", "packages/fe-common/src/utils/hazard/hazardPointTransformers.ts", "packages/fe-common/src/utils/hazard/index.ts"]
---

# Consolidate hazard types and utils into fe-common

## Motivation
Hazard types and 14 utility functions were defined separately in web and mobile with diverging fields. structureVersion was hardcoded differently on each platform.

## What changed
Moved type definitions into fe-common with union of web + mobile fields. Consolidated 14 utility functions. Web and mobile re-export for backward compatibility. Fixed structureVersion to flow from API response.

## Why this approach
- Single source of truth prevents drift. Re-export pattern preserves existing import paths.
- Flow structureVersion from API — backend owns the version.
- normalizeEnergySourceType handles legacy API values at runtime.

## Lessons
- Type drift happens when shared types live in multiple places. Web added selected field, mobile added imageFiles — neither saw the other's changes.
- Hardcoded version numbers break when backend changes schema. Always flow from API response with fallback for old data.
- Union types (version: 1 | 2) are better than optional fields for discriminated unions.

## If you're working on something similar
- Define shared types once in fe-common and re-export from consumers.
- When consolidating duplicated functions, diff both implementations line-by-line.
- Use normalizeX functions for legacy API value mapping.
- Test cross-platform builds after consolidation.
