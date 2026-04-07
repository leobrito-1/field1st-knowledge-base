---
project: field1st
repo: rtslabs/field1st
pr: 119
branch: feature/mobile-rn081-expo54-upgrade
date: 2026-03-09
author: andy.ewald
packages: [mobile]
tags: [mobile, react-native, typescript]
related: [2026-03-17-rn-083-expo-55-new-arch]
answers: ["TextInputFocusEventData module not found", "expo-file-system import not found after Expo upgrade", "isHermesEnabled return type mismatch Java", "jcenter repository deprecated Gradle"]
---

# Upgrade React Native 0.79 to 0.81 / Expo 53 to 54

## Motivation
RN 0.81 is the last version supporting Legacy Architecture before mandatory New Architecture in 0.83+. This positions the app for future migration while picking up React 19.1 improvements.

## What changed
Upgraded RN 0.79.3 to 0.81.5, Expo 53 to 54, React to 19.1. Pinned Reanimated to 3.x. Upgraded Android build tools and iOS Firebase SDK. Migrated deprecated APIs.

## Why this approach
- Staged migration: 0.79 to 0.81 (this PR) then 0.83 + New Arch (next PR). Splitting reduces blast radius.
- Pin Reanimated 3.x because 4.x requires New Architecture.

## Lessons
- TextInputFocusEventData type was removed in RN 0.81. Replace with NativeSyntheticEvent<TargetedEvent>.
- isHermesEnabled() must return primitive boolean, not Boolean wrapper (Java 17 enforcement).
- Removed jcenter() from build.gradle — deprecated since 2021, finally removed in AGP 8.11.
- iOS Podfile: Reanimated C++ flags must use $(OTHER_CFLAGS) reference, not hardcoded replacement.

## If you're working on something similar
- Run yarn tsc && yarn test before and after upgrade.
- On iOS: delete Pods/ and Podfile.lock, then pod install --repo-update.
- Search codebase for expo-file-system imports without /legacy suffix.
