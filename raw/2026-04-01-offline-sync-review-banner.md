---
project: field1st
repo: rtslabs/field1st
jira: F1-235
pr: 382
branch: feature/F1-235-mobile-sync-review-banner
date: 2026-04-01
author: andy.ewald
packages: [mobile, fe-common]
tags: [mobile, react-native, redux]
related: []
answers: ["offline documents not visible after sync", "created document offline but cant find it", "Needs Review banner not appearing"]
files: ["packages/mobile/src/core/components/documents/DocumentsResults.tsx", "packages/mobile/src/core/navigation/Navigation.tsx", "packages/mobile/src/shared/components/NeedsReviewBanner/NeedsReviewBanner.styles.ts", "packages/mobile/src/shared/components/NeedsReviewBanner/NeedsReviewBanner.tsx", "packages/mobile/src/shared/hooks/useNeedsReviewDocIds.ts"]
---

# Mobile offline sync review banner

## The problem
Documents created offline get flagged Needs Review after syncing. Users on Dashboard or other tabs had no visibility into flagged documents unless they navigated to Documents list.

## What we did
Added persistent warning banner across all main tabs showing document count. Tapping navigates to Documents list where items are pinned with yellow background. Banner auto-hides on Documents tab.

## Why this way and not another
- Extracted shared useNeedsReviewDocIds hook to deduplicate logic.
- Reuses existing Redux offlineStorage.documentSyncStatuses state.

## What we learned
- Document count computation covers both VLM placeholder IDs and explicit needsReview flags. Must check syncStatus === Success or Finished to avoid showing banner during active sync.
- Navigation state detection requires checking nested route state, not just activeTab.name.

## Technical reference
- Use useNavigationState selector to detect current screen and conditionally hide UI.
- Extract shared selectors when two components need the same derived state from Redux.
