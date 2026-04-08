---
project: field1st
repo: rtslabs/field1st
jira: F1-225
pr: 362
branch: feature/F1-225-android-ready1st-widget
date: 2026-03-30
author: andy.ewald
packages: [mobile]
tags: [mobile, react-native]
related: []
answers: ["Android home screen widget not updating", "widget configuration activity not appearing", "Material You colors crash on pre-Android 12", "POST_NOTIFICATIONS permission missing"]
files: ["packages/mobile/android/app/src/main/AndroidManifest.xml", "packages/mobile/android/app/src/main/java/com/rtslabs/field1st/MainApplication.java", "packages/mobile/android/app/src/main/java/com/rtslabs/field1st/Ready1stActivityModule.java", "packages/mobile/android/app/src/main/java/com/rtslabs/field1st/Ready1stNotificationService.java", "packages/mobile/android/app/src/main/java/com/rtslabs/field1st/Ready1stWidgetConfigActivity.java"]
---

# Android Ready1st home screen widget and ongoing notification

## Motivation
iOS had full Ready1st widget support but Android had none. Users on Android couldn't see Ready1st status without opening the app.

## What changed
Added native Android AppWidgetProvider, ongoing foreground notification, Material You theming with dynamic colors, and widget configuration activity. All Java + XML, no TypeScript changes.

## Why this approach
- SharedPreferences as bridge: RN writes, native widget reads.
- Foreground service for persistent notification matches iOS Live Activity semantics.
- drawable-v31/ for Material You with fallback on older devices.

## Lessons
- React Native native modules need manual package registration in MainApplication.java.
- Widgets don't auto-update when app state changes. Must explicitly broadcast via AppWidgetManager.
- Material You colors only exist on Android 12+. Need fallback drawables or widget crashes.
- POST_NOTIFICATIONS permission required on Android 13+. Missing permission causes silent failure.

## If you're working on something similar
- Use SharedPreferences as RN-to-widget bridge.
- Broadcast ACTION_APPWIDGET_UPDATE after writing to SharedPreferences.
- Use foreground service for persistent notifications.
- Test on Android 12+ and pre-12 for drawable fallback.
