---
project: field1st
repo: rtslabs/field1st
pr: 336
branch: chore/mobile-web-debug-investigation
date: 2026-03-26
author: andy.ewald
packages: [mobile]
tags: [mobile, react-native, web, testing]
related: []
answers: ["React Native app not running in browser", "Platform.OS is undefined in web build", "AsyncStorage not available on web", "Metro bundler not resolving .web.ts files"]
files: ["packages/mobile/src/core/App.tsx", "packages/mobile/src/core/AppWrapper.tsx", "packages/mobile/src/core/components/document/DocumentFullPageContent.tsx", "packages/mobile/src/core/components/document/DocumentSectionContent.tsx", "packages/mobile/src/core/nativeModules/ArcGISFeatureModule.web.ts"]
---

# Enable Expo Web for Playwright debugging

## The problem
Playwright E2E tests need a web-accessible UI. Enabling Expo Web allows the mobile app to render in a browser for debugging and E2E tests without forking the codebase.

## What we did
Added web platform support via Expo SDK 55 Metro-for-Web. Created 25 web stubs for native-only modules. Configured Metro resolveRequest to swap native imports for .web.ts stubs. Zero changes to existing imports.

## Why this way and not another
- Metro resolveRequest over manual imports: keeps all existing import statements unchanged.
- Stubs not polyfills: no-op functions avoid bundling megabytes of unused native code.
- Development/debugging only, not a production web app.

## What we learned
- Metro resolveRequest must check context.platform === 'web' and return filePath with .ts extension — without extension Metro can't find the file.
- AsyncStorage needs a web stub returning in-memory Map — localStorage causes Redux Persist quota exceeded errors with large state.
- @expo/vector-icons fonts don't load on web by default — must inject via @font-face in index.web.js.
- KeyboardAvoidingView doesn't work on web — use ScrollView with flexGrow instead.

## Technical reference
- Create stubs for all native modules first, then gradually implement web-compatible versions.
- Use metro.config.js resolveRequest hook to swap modules per platform.
- For Redux Persist on web, use in-memory storage adapter.
- Delete .expo/ cache if Metro bundler hangs.
