---
project: field1st
repo: rtslabs/field1st
jira: F1-232
pr: 373
branch: fix/F1-232-mobile-offline-detection
date: 2026-03-31
author: andy.ewald
packages: [mobile]
tags: [mobile, react-native]
related: [2026-03-31-airplane-mode-recovery]
answers: ["airplane mode detection slow", "offline banner takes 60 seconds to appear", "NetInfo slow to update", "isInternetReachable delay"]
---

# Faster airplane mode offline detection via NetInfo tuning

## Motivation
App relied on NetInfo default 60-second reachabilityLongTimeout. When airplane mode was toggled, the app waited up to 60s for HTTP-based isInternetReachable to fail.

## What changed
Shorter NetInfo polling intervals (60s to 15s online, 5s to 3s offline). Added isConnected === false check — OS-level signal that fires near-instantly on airplane mode. Fixed Storm AppWrapper missing dispatch() call. Added reducer short-circuit for noisy events.

## Why this approach
- isConnected is OS-level, updates instantly on airplane mode.
- Reducer short-circuit prevents re-renders from wifi signal fluctuations.
- Storm AppWrapper called handleConnectivityChange without dispatch(). Action objects were silently dropped.

## Lessons
- NetInfo provides multiple signals at different speeds. isConnected (OS, instant) vs isInternetReachable (HTTP, slow). Check fast signals first.
- Action creators return action objects. Must be dispatched. Calling without dispatch() is a silent no-op.
- NetInfo fires on every wifi signal strength change. Short-circuit reducer when state hasn't meaningfully changed.

## If you're working on something similar
- Check both isConnected (fast) and isInternetReachable (slow) signals.
- Short-circuit reducers when state hasn't meaningfully changed.
- Configure NetInfo with shorter intervals (15s online, 3s offline).
- Verify action creators are dispatched — calling without dispatch() is silent.
