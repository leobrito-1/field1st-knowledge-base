---
project: field1st
repo: rtslabs/field1st
jira: F1-182
pr: 262
branch: feature/F1-182-web-saved-transcripts
date: 2026-03-18
author: andy.ewald
packages: [fe-common, web, mobile]
tags: [fe-common, web, mobile, typescript, react, react-native]
related: []
answers: ["transcripts disappear after page refresh", "microphone icon not showing on documents with pending transcripts", "mobile and web transcript storage drifting"]
files: ["packages/fe-common/src/api/storage/index.ts", "packages/fe-common/src/api/storage/transcriptQueue.ts", "packages/mobile/src/core/DataWrapper.tsx", "packages/mobile/src/core/components/Voice1st/Voice1stComponent.tsx", "packages/mobile/src/core/components/Voice1st/Voice1stDrawer.tsx"]
---

# Voice1st transcript auto-save and shared queue

## The problem
Mobile had transcript auto-save but web transcripts were session-only. Each platform had its own queue implementation causing drift.

## What we did
Extracted transcript queue logic into fe-common/src/api/storage/transcriptQueue.ts with cross-platform storage adapter. Web now auto-saves transcripts with Saved Transcripts menu and mic icons on pending documents.

## Why this way and not another
- fe-common module prevents platform drift, uses storage adapter (localStorage on web, AsyncStorage on mobile).
- Auto-save on stop recording — users expect drafts to persist without explicit Save button.

## What we learned
- Migrating storage keys across platforms breaks existing saved data. Mobile transcripts in old format orphaned but harmless.
- Auto-save + manual dequeue needs explicit cleanup in two places: after document creation and after Process Voice.
- localStorage keys should be namespaced (field1st_transcript_queue) to avoid collisions.

## Technical reference
- Use storage adapter pattern in fe-common for cross-platform storage.
- Auto-save immediately on user action, not on component unmount.
- Dequeue saved items after successful processing in all code paths.
- Clear saved items on logout to prevent cross-user contamination.
