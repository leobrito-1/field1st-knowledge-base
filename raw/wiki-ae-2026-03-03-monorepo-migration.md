---
project: field1st
repo: rtslabs/field1st
pr: 153
branch: feature/migrate-repos-to-monorepo
date: 2026-03-03
author: andy.ewald
packages: [infra, cli]
tags: [infra, ci-cd]
related: []
answers: ["git subtree merge conflict", "namespaced git tags not showing up", "stale un-namespaced tags after git fetch"]
---

# Migrate reporting-view, infra, and cli repos into monorepo

## Motivation
Three separate repositories were maintained independently, creating coordination overhead for cross-repo changes and inconsistent versioning.

## What changed
Used git subtree add to import three repos into packages/ with full commit history. Imported 43 tags with namespace prefixes to avoid collisions.

## Why this approach
- git subtree over submodules: embeds full history, no external dependencies.
- Namespaced tags prevent collisions.
- One-time import, source repos archived.

## Lessons
- After git fetch with tag imports, 37 un-namespaced tags leaked into the local repo. Had to manually delete stale tags after import.
- git subtree add creates a merge commit preserving ability to trace back to original repo's history.

## If you're working on something similar
- Use git subtree add --prefix=packages/<name> <remote> <branch> to import with full history.
- Namespace tags before import to avoid collisions.
- After import, clean leaked tags: git tag -l | grep -v '^prefix' | xargs git tag -d.
