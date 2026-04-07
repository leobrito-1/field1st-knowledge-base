---
project: field1st
repo: rtslabs/field1st
jira: F1-166
pr: 240
branch: feature/F1-166-rn-083-expo-55-upgrade
date: 2026-03-17
author: andy.ewald
packages: [mobile]
tags: [mobile, react-native, typescript]
related: [2026-03-09-rn-081-expo-54-upgrade]
answers: ["Android New Architecture native module returns null", "react-native-voice TurboModule not found Android", "autolinking failed after React Native upgrade", "react-native-reanimated 4.x worklets not found"]
---

# Upgrade React Native 0.81 to 0.83 + Expo 55 + Android New Architecture

## Motivation
RN 0.83 and Expo 55 mandate New Architecture on Android. Required to stay on supported Expo SDK and enables Fabric renderer and TurboModules.

## What changed
Upgraded RN to 0.83.2, Expo to 55, Reanimated to 4.2.2. Enabled Android New Architecture. Migrated from manual linking to autolinking (removed 25+ module registrations). Deleted 280 lines of dead polyfills.

## Why this approach
- New Architecture on Android only — iOS uses interop layer, reducing risk.
- Autolinking replaces error-prone manual linking.
- Reanimated 4.x requires separate react-native-worklets package.

## Lessons
- react-native-voice resolves to null on Android with New Architecture — uses legacy NativeModules bridge with no TurboModule support. Voice1st broken on Android until library updates.
- Autolinking suppressions in react-native.config.js must be removed when migrating — leaving them causes module not found crashes.
- settings.gradle manual include blocks conflict with autolinking. Remove all except truly manual modules.
- Reanimated 4.x worklets require import 'react-native-worklets' at top of files using worklet directive.

## If you're working on something similar
- Audit all native modules for TurboModule/Fabric support before enabling newArchEnabled=true.
- Remove all autolinking suppressions from react-native.config.js.
- Run ./gradlew clean on Android and delete Pods/ on iOS after changing newArchEnabled.
- If a native module breaks, check for codegenConfig in its package.json.
