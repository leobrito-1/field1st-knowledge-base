---
project: field1st
repo: rtslabs/field1st
jira: F1-180
pr: 345
branch: feature/F1-180-offline-create-document
date: 2026-03-27
author: andy.ewald
packages: [mobile]
tags: [mobile, react-native, redux]
related: [2026-03-24-vlm-offline-scan]
answers: ["Start Document from hazard assessment fails when offline", "document creation shows error in airplane mode", "hazard data lost after going offline"]
files: ["packages/mobile/src/core/api/document/getDocuments.ts", "packages/mobile/src/core/components/documents/DocumentsResults.tsx", "packages/mobile/src/core/data/asyncStorage/asyncStorage.ts", "packages/mobile/src/core/data/syncQueuedOfflineActions.ts", "packages/mobile/src/core/screens/NewDocumentDrawer.tsx"]
---

# Offline queue for document creation from hazard data

## Motivation
Creating a document from hazard data while offline would fail silently or show an error inside the drawer which immediately closed. Needed to match the VLM offline pattern.

## What changed
When offline, the app queues createDocumentFromData, shows a placeholder in Documents list with sync icon. On reconnect, syncs automatically and replaces placeholder with real document.

## Why this approach
- Follows established VLM placeholder pattern for consistency.
- Promise.all for parallel placeholder fetches.

## Lessons
- Namespace collision: copy-pasted toast code used vlm: key for doc-from-data. Changed to newDocument.offlineDocSynced.
- AsyncStorage prefix constants: clearOfflineStorageExceptModifiedDocs needs to preserve both VLM and doc-from-data prefixes.
- Context-aware toasts: tap handler must differentiate placeholder types using isVlmPlaceholderId() and isDocFromDataPlaceholderId().

## If you're working on something similar
- Export prefix constants from placeholder modules for cleanup logic.
- Fetch multiple placeholder types in parallel with Promise.all.
- Use context-aware toast messages based on placeholder type.
