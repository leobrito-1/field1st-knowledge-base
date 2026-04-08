---
project: field1st
repo: rtslabs/field1st
jira: F1-181
pr: 319
branch: feature/F1-181-vlm-offline-scan
date: 2026-03-24
author: andy.ewald
packages: [mobile]
tags: [mobile, react-native, redux]
related: []
answers: ["VLM scan fails when offline", "Start from Scan shows error in airplane mode", "iOS picker buttons unresponsive after first use", "scanned files lost after navigation offline"]
files: ["packages/mobile/src/core/api/document/getDocuments.ts", "packages/mobile/src/core/components/documents/DocumentsResults.tsx", "packages/mobile/src/core/data/syncQueuedOfflineActions.ts", "packages/mobile/src/core/screens/NewDocumentDrawer.tsx", "packages/mobile/src/core/screens/launchpad/NewDocumentView.tsx"]
---

# VLM offline scan with document list placeholder and sync status

## Motivation
VLM scans should queue gracefully when offline with clear visual feedback about sync state, matching the existing offline document creation pattern.

## What changed
When offline, VLM scans save files to filesystem (vlm-queue/ directory) and a placeholder appears in the document list with sync status icons. On reconnect, files upload and placeholder transitions to real document.

## Why this approach
- Filesystem storage persists across app restarts.
- Discriminated VlmSubmitResult union lets UI handle each case explicitly.
- Concurrency lock prevents double-sync when multiple effects fire on offline-to-online transition.

## Lessons
- iOS picker hide/show state dance caused unresponsive buttons. Removed dance, pickers now call hook functions directly.
- Discriminated unions over booleans: returning { success, offlineQueued, data, error } caused ambiguous states. Switched to discriminated union with status field.
- Must removeVlmPlaceholder from AsyncStorage after sync completes, otherwise stale placeholders persist.

## If you're working on something similar
- Use discriminated unions for async result types.
- Store queued files to filesystem, not base64 in AsyncStorage.
- Add concurrency locks when multiple code paths can trigger the same async operation.
