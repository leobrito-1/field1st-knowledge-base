---
project: field1st
repo: rtslabs/field1st
jira: F1-247
pr: 391
branch: fix/F1-247-mobile-offline-sync-conflict
date: 2026-04-03
author: andy.ewald
packages: [mobile]
tags: [mobile, react-native]
related: []
answers: ["offline edits overwrite server changes", "admin edits lost after mobile sync", "conflict prompt not appearing", "mobile sync silently overwrites web changes"]
files: ["packages/mobile/src/core/data/syncOfflineDocuments.ts", "packages/mobile/src/shared/data/syncHelpers.ts", "packages/mobile/src/storm/data/syncOfflineDocuments.ts"]
---

# Per-document timestamp conflict detection for offline sync

## The problem
Conflict detection only triggered when the same user edited on both platforms. Admin edits on web were silently overwritten by mobile offline sync. Root cause: global lastSuccessfulSync timestamp was role-dependent.

## What we did
Replaced global timestamp with per-document comparison. New hasServerDocumentChanged() compares stored offline timestamps (dateLastSubmitted + lastModifiedDate) against fresh server document.

## Why this way and not another
- Per-document timestamps are authoritative, not dependent on user role or global sync state.
- Compare both dateLastSubmitted and lastModifiedDate because either can change independently.
- After conflict resolution, refresh local cache with server version.

## What we learned
- Global sync timestamps coupled to user sessions create blind spots for cross-user edits. Per-resource timestamps decouple sync from user identity.
- Nullish timestamps require explicit null-coalescing in comparisons. null !== undefined in strict equality.

## Technical reference
- Compare document-level timestamps rather than global sync watermarks.
- Handle null/undefined timestamp fields explicitly with null-coalescing.
- After conflict resolution, refresh local cache with winning version.
- Test cross-user conflicts (admin vs field user) and same-user cross-device conflicts.
