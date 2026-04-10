---
project: field1st
repo: rtslabs/field1st
pr: 172
branch: feature/hazard-assessment-side-drawer
date: 2026-03-05
author: andy.ewald
packages: [fe-common, web, mobile, service]
tags: [fe-common, web, mobile, spring-boot, react, react-native]
related: []
answers: ["documents not filtering by hazard analysis ID", "nested drawer renders behind first drawer", "Paper Menu not working with Skia Canvas"]
files: ["packages/fe-common/src/api/hazard/hazardAnalysisResource.ts", "packages/fe-common/src/types/api/documentRequestParameters.ts", "packages/fe-common/src/types/api/documentSummaryVm.ts", "packages/mobile/src/core/components/documents/DocumentSideDrawer.tsx", "packages/mobile/src/core/components/hazardAssessments/HazardAssessmentSideDrawer.styles.ts"]
---

# Hazard assessment side drawer with related documents

## The problem
Hazard assessments used popup menus (web) and inconsistent patterns (mobile). No way to see which documents were created from a hazard assessment.

## What we did
Replaced popup menus with side drawers on both platforms. Added backend filter createdFromHazardAnalysisId to /api/documents. Web shows nested drawer, mobile uses separate screen. Migrated web styles to Figma design tokens.

## Why this way and not another
- Backend filter instead of client-side — scales to large datasets.
- Nested drawer (web) vs separate screen (mobile) — web has viewport space, mobile uses navigation stack.
- fe-common API functions prevent web/mobile drift.

## What we learned
- Adding a filter to a paginated endpoint requires touching DTO, query builder, and repository. Test with pagination params to ensure filter applies before pagination slice.
- Nested drawers need explicit z-index management.
- i18n keys for shared UI go in fe-common src/i18n/, not directly in web or mobile locales.

## Technical reference
- For backend filters on foreign keys, add DTO field + query predicate + repository method.
- Test with ?page=0&size=10 to verify filter applies before pagination.
- Mobile: use Alert.alert for destructive actions (Paper Menu doesn't work with Skia Canvas).
