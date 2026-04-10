---
project: field1st
repo: rtslabs/field1st
jira: F1-248
pr: 392
branch: feature/aewald/form-builder-dataset-options-expand
date: 2026-04-02
author: andy.ewald
packages: [fe-common, web, mobile]
tags: [fe-common, web, mobile, typescript, react, react-native]
related: []
answers: ["defenses not showing for dataset answer options", "selection lookup failing for dataset-based questions", "dataset options not editable in form builder"]
files: ["packages/fe-common/src/functions/util/dataSource.ts", "packages/fe-common/src/functions/util/dataSourceSelectionMerge.ts", "packages/fe-common/src/functions/util/formEntity.ts", "packages/fe-common/src/functions/util/index.ts", "packages/fe-common/src/hooks/useSelectedTags.ts"]
---

# Form builder dataset options expansion and selection lookup fix

## The problem
Form builder had no way to view or configure dataset options. At document fill time, the selection lookup failed for dataset options because associatedId doesn't match selection.id for dataset values, causing defenses and OE tags to not display.

## What we did
Added Expand options toggle in form builder showing dataset items as editable cards. Fixed selection lookup in all field components to use selection.rootId === response.associatedRootId as fallback.

## Why this way and not another
- rootId fallback: associatedRootId points to dataset value ID which matches selection.rootId.
- mergeSelectionsWithDataSourceItems enriches dataset items with selection metadata.

## What we learned
- Selection lookup for dataset options requires two-step check: selection.id (custom) OR selection.rootId (dataset). Missing fallback caused defenses/OE/media to silently fail.
- Dataset items don't have selection IDs until saved. Form builder synthesizes temporary IDs for UI rendering.
- Mobile and web had identical broken logic in 8+ files. Fix must touch all field components.

## Technical reference
- Always check both selection.id and selection.rootId against response IDs.
- Grep for all usages of broken pattern across web, mobile, and fe-common before claiming fixed.
- Add explicit tests for dataset vs custom option behavior — they follow different code paths.
