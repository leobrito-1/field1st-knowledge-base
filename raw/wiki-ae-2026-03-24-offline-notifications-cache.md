---
project: field1st
repo: rtslabs/field1st
jira: F1-210
pr: 318
branch: fix/F1-210-offline-notifications-caching
date: 2026-03-24
author: andy.ewald
packages: [mobile]
tags: [mobile, react-native]
related: []
answers: ["useNotifications fails when offline", "push notification retry manager loops forever offline", "notifications show nothing in airplane mode"]
files: ["packages/mobile/src/core/components/notifications/notificationRetryManager.ts", "packages/mobile/src/core/components/notifications/useNotifications.ts", "packages/mobile/src/core/data/asyncStorage/offlineActions.ts", "packages/mobile/src/core/data/asyncStorage/offlineNotifications.ts"]
---

# Cache notifications for offline use

## Motivation
The useNotifications hook, forceRefresh, push notification retry manager, and foreground listener all called the API without checking offline status, causing failed network requests while offline.

## What changed
Cache notifications in AsyncStorage. When offline, serve cached notifications. Added notifications to background sync lifecycle.

## Why this approach
- Write-through cache on every successful fetch keeps data fresh.
- Offline guard in retry manager stops retry cycle when device goes offline.

## Lessons
- All network paths need offline guards: mount, forceRefresh, retry, foreground listener.
- Optimistic mark-as-read shows instant feedback offline by updating local state.
- Retry loop waste: notificationRetryManager kept retrying while offline. Added selectIsOffline guard.

## If you're working on something similar
- Check offline state before every API call, including retry logic and event listeners.
- Use write-through caching (update cache on every successful fetch).
- Stop retry loops when offline to save battery and avoid error noise.
