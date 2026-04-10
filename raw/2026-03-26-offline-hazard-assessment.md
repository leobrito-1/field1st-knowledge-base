---
project: field1st
repo: rtslabs/field1st
jira: F1-179
pr: 334
branch: feature/F1-179-offline-hazard-custom-entry
date: 2026-03-26
author: andy.ewald
packages: [fe-common, mobile, web]
tags: [mobile, web, fe-common, react-native, redux]
related: []
answers: ["hazard assessment shows nothing when offline", "modal shows Error Analyzing Image instead of offline UX", "custom hazards disappear after AI analysis", "energy sources not syncing between web and mobile"]
files: ["packages/fe-common/src/functions/hazardAnalysis/hazardAnalysisStatus.ts", "packages/fe-common/src/functions/hazardAnalysis/index.ts", "packages/fe-common/src/i18n/index.ts", "packages/fe-common/src/index.ts", "packages/fe-common/src/utils/hazard/hazardPointTransformers.ts"]
---

# Offline hazard assessment support with cross-platform sync

## The problem
Mobile users in the field face unreliable connectivity. The hazard assessment list failed silently when offline. Assessments created offline vanished on navigation. The modal showed a generic error instead of proper offline UX.

## What we did
Full offline support: cache list for offline viewing, create assessments offline with manual hazard entry, persist images to filesystem, auto-sync on reconnect with conflict resolution. Shared status/display logic moved to fe-common.

## Why this way and not another
- Shared helpers in fe-common ensure web and mobile handle statuses identically.
- Conflict resolution compares lastModifiedDate to detect server-side changes.
- Offline-created items use negative temp IDs to distinguish from server records.

## What we learned
- Race condition: Modal visibleHazards prop didn't update when hazards changed post-analysis. Added useEffect to sync.
- Energy sources cross-platform bug: transformers weren't reading/writing energySources from/to API. Fixed in both directions.
- Custom hazard loss: AI analysis response replaces hazardPoints array, dropping manual entries. Extract before analysis, merge after.

## Technical reference
- Use enrichHazardAnalysis / getStatusText / getStatusColor for all status display.
- Preserve custom data before calling AI endpoints that overwrite fields.
- Compare lastModifiedDate for conflict detection on offline-edited records.
- Use negative IDs for offline-created placeholder records.
