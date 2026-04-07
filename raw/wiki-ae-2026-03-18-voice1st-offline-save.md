---
project: field1st
repo: rtslabs/field1st
jira: F1-178
pr: 258
branch: feature/F1-174-saved-transcripts-launchpad
date: 2026-03-18
author: andy.ewald
packages: [mobile]
tags: [mobile, react-native, redux]
related: []
answers: ["Voice1st fails when offline", "transcript vanished after closing drawer", "Android 10 mic button unresponsive after tapping", "offline voice recording lost on navigation"]
---

# Offline Voice1st save with Saved Transcripts list

## Motivation
Users want to record voice notes but may be offline. The previous approach showed intrusive one-at-a-time Alerts on reconnect. In-document Voice1st had no offline handling at all.

## What changed
Added Saved Transcripts menu in launchpad. Users save transcripts online or offline, review from scrollable list, process when ready. Shared offlineActionQueue infrastructure handles queuing.

## Why this approach
- offlineActionQueue generic API supports voice1st, doc_from_data, vlm subtypes.
- Auto-save after recording stops (debounced 500ms).
- BottomDrawer disableScroll prop prevents scroll conflicts with FlatList.

## Lessons
- Android 10 Fabric touch regression: Animated.View with pointerEvents="none" inside TouchableOpacity caused unresponsive mic button. Moved glow out, switched to Pressable.
- Duplicate locale key: second "common" key in en.json overwrote first, losing alert/cancel/openSettings translations. Merged keys.
- persistentTranscript.current retained text across drawer open/close, preventing loss on navigation.

## If you're working on something similar
- Use offlineActionQueue for any queued offline work.
- Debounce auto-save after recording stops to let final transcript segments settle.
- Move animated overlays out of touchable components on Android to avoid Fabric hit-test issues.
