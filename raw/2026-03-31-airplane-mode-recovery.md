---
project: field1st
repo: rtslabs/field1st
jira: F1-232
pr: 371
branch: feature/F1-232-fix-offline-online-recovery
date: 2026-03-31
author: andy.ewald
packages: [fe-common, mobile]
tags: [mobile, react-native, fe-common]
related: [2026-03-31-airplane-mode-detection]
answers: ["app freezes after airplane mode toggle", "blank screen after going offline", "duplicate documents created after sync", "offline photos not persisting", "force close required after airplane mode"]
files: ["packages/fe-common/src/api/network.ts", "packages/mobile/src/core/DataWrapper.tsx", "packages/mobile/src/core/components/document/Section.tsx", "packages/mobile/src/core/data/createOfflineDocument.ts", "packages/mobile/src/core/data/syncOfflineDocuments.ts"]
---

# Fix mobile airplane mode recovery cascade failures

## The problem
QA reported app becomes unresponsive after toggling airplane mode off — blank screen requiring 3+ force-closes. Offline photo uploads showed success but didn't persist. Reconnecting created duplicate documents. Root cause: fetch() calls hang indefinitely when TCP connections break.

## What we did
Seven fixes: fetchWithTimeout() wrapper with 30s AbortController, treat isInternetReachable === null as online, timestamp-based sync locks (60s auto-release), 15s timeout on waitForReduxState, consolidate duplicate useAsyncEffect hooks, persist syncedServerId immediately after createDocument, initialize offlinePhotos array.

## Why this way and not another
- AbortController timeout prevents hung fetch on broken TCP.
- Timestamp locks auto-release after 60s, recovering from crashes. Boolean locks never recovered.
- isInternetReachable === null means checking, not offline. Treating as offline delayed transitions by 60s.
- syncedServerId persistence makes document creation idempotent.

## What we learned
- Native fetch() doesn't timeout on broken TCP (airplane mode mid-request). Wrap all fetch() with AbortController-based timeout at network layer.
- Boolean locks without timeout are permanent deadlocks. Use timestamp-based locks with auto-release.
- Duplicate useAsyncEffect hooks in one component create race conditions. Consolidate into single effect.
- Idempotent sync requires persisting server-assigned IDs immediately, not waiting until end of multi-step sync.

## Technical reference
- Wrap all fetch() calls with AbortController-based timeout (30s).
- Use timestamp-based locks with auto-release (60s) for critical sections.
- Treat isInternetReachable === null as checking (online), not offline.
- Persist server-assigned IDs immediately after creation.
