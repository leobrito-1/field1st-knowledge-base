---
project: field1st
repo: rtslabs/field1st
pr: 87
branch: feature/gha-deploy-refactoring
date: 2026-02-23
author: andy.ewald
packages: [service]
tags: [ci-cd, infra]
related: []
answers: ["GitHub Actions Slack notification not triggering", "Docker build running twice for same commit", "ECS task definition not updating after docker push", "deploy workflow taking too long"]
---

# Consolidate deploy workflows with shared Slack action and image caching

## Motivation
Seven deploy workflows had ~3000 lines of duplicated Slack notification YAML. Docker builds ran redundantly when deploying the same commit to multiple environments.

## What changed
Created composite Slack action with start/update/finish operations. Added ECR image caching — check for git_<SHA> tag before building. Created shared multi-stage Dockerfile via BUILD_MODULE arg. Reduced ~1949 lines net.

## Why this approach
- Composite action for Slack reuse across 7 workflows.
- Delete + repost for final Slack notification triggers push notifications (edits don't).
- ECR describe-images is ~200ms — avoids 5-10 minute Docker rebuild for same commit.

## Lessons
- Slack Bot Token API requires chat:write scope and bot must be invited to channel first.
- GitHub Actions composite actions can't use secrets directly — pass as inputs from calling workflow.
- ECR image caching: use git rev-parse HEAD for SHA, then aws ecr describe-images. Exit 0 means image exists.

## If you're working on something similar
- Tag Docker images with git_<SHA> during build for caching.
- Run aws ecr describe-images before docker build — exit 255 means not found.
- For multi-stage Dockerfiles, declare ARG BUILD_MODULE before FROM.
