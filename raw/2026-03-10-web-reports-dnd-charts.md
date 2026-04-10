---
project: field1st
repo: rtslabs/field1st
pr: 207
branch: feature/web-reports-page-enhancements
date: 2026-03-10
author: andy.ewald
packages: [web]
tags: [web, react, typescript]
related: []
answers: ["chart preferences not persisting", "drag and drop not working in CSS Grid", "pinned cards losing sort order"]
files: ["packages/web/packages/field-first/src/components/clientAdmin/reports/FormReport/BarChartResponse.module.scss", "packages/web/packages/field-first/src/components/clientAdmin/reports/FormReport/BulkActionsToolbar.module.scss", "packages/web/packages/field-first/src/components/clientAdmin/reports/FormReport/BulkActionsToolbar.tsx", "packages/web/packages/field-first/src/components/clientAdmin/reports/FormReport/ChartSection.module.scss", "packages/web/packages/field-first/src/components/clientAdmin/reports/FormReport/ChartTypeToggle.module.scss"]
---

# Reports page drag-and-drop cards with chart toggles

## The problem
The reports page had fragmented card styling, no way to reorder summary cards or pin favorites, and fixed chart types per question.

## What we did
Added drag-and-drop reordering with pinning using @hello-pangea/dnd, per-card chart type toggles, bulk actions toolbar, unified card styling. Persisted to localStorage.

## Why this way and not another
- @hello-pangea/dnd for DnD — mature, accessible, works with two-column grids.
- localStorage for persistence — no backend needed.
- Imperative ref pattern for parent-triggered bulk actions.

## What we learned
- DnD in CSS Grid layouts requires explicit display: flex on droppable columns to prevent layout collapse during drag.
- Store drag order as {questionId: sortIndex} map, not array indices — indices break when items added/removed.
- Use refs for values that polling/intervals need to read — setInterval closures capture stale state.

## Technical reference
- Use @hello-pangea/dnd with droppableId per column for multi-column grids.
- Store order as ID-to-index map in localStorage.
- For bulk actions, expose imperative ref with methods.
