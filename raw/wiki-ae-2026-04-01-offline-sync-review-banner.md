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
---

# Mobile offline sync review banner

## Motivation
Documents created offline get flagged Needs Review after syncing. Users on Dashboard or other tabs had no visibility into flagged documents unless they navigated to Documents list.

## What changed
Added persistent warning banner across all main tabs showing document count. Tapping navigates to Documents list where items are pinned with yellow background. Banner auto-hides on Documents tab.

## Why this approach
- Extracted shared useNeedsReviewDocIds hook to deduplicate logic.
- Reuses existing Redux offlineStorage.documentSyncStatuses state.

## Lessons
- Document count computation covers both VLM placeholder IDs and explicit needsReview flags. Must check syncStatus === Success or Finished to avoid showing banner during active sync.
- Navigation state detection requires checking nested route state, not just activeTab.name.

## If you're working on something similar
- Use useNavigationState selector to detect current screen and conditionally hide UI.
- Extract shared selectors when two components need the same derived state from Redux.
