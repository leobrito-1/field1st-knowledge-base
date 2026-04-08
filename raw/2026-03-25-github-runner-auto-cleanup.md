---
project: field1st
repo: rtslabs/field1st
pr: 327
branch: feature/runner-replacement-cleanup
date: 2026-03-25
author: leo.brito
packages: [infra]
tags: [ci-cd, infra]
related: []
answers: ["GitHub Actions runner went offline after 36 days", "No space left on device on self-hosted runner", "Self-hosted runner not picking up jobs"]
files: ["infra/github-runner/replace-runner.sh", "infra/github-runner/setup.sh"]
---

# Fix offline GitHub Actions runner — add auto-cleanup and replacement script

## Motivation
The self-hosted runner (`service-deploy` label, NONPROD account) went offline after 36 days. Root cause: 50 GB disk filled from Docker images, Gradle caches, and runner `_work/` directories with no cleanup mechanism.

## What changed
Added post-job cleanup hook (`ACTIONS_RUNNER_HOOK_JOB_COMPLETED`), CloudWatch Agent for disk/memory metrics, journald 500MB cap, daily safety-net cron, and a `replace-runner.sh` script that launches a new instance, verifies it's online, then terminates the old one.

## Why this approach
- Post-job hook over cron: cleanup runs immediately after every job, not on a fixed schedule.
- CloudWatch logs: cleanup output visible in `/github-runner/cleanup` log group for debugging without SSH.
- Replace-then-terminate: launching new instance first ensures zero additional downtime.

## Lessons
- Docker images, Gradle caches, and runner `_work/` directories grow unbounded without cleanup. After 36 days: Docker ~30 GB, Gradle ~10 GB, `_work/` ~5 GB.
- SSM commands silently fail when disk is full — you can't even SSH or run diagnostics. CloudWatch metrics would have caught this early.
- `docker image prune -a` is too aggressive (removes all unused images). Use `--filter "until=24h"` to keep recently pulled images for cache reuse.
- The runner systemd service name follows the pattern `actions.runner.<org>-<repo>.<hostname>.service`. The hook is injected via a systemd drop-in file.

## If you're working on something similar
- Use `ACTIONS_RUNNER_HOOK_JOB_COMPLETED` to run cleanup after every job via a systemd drop-in.
- Monitor disk with CloudWatch Agent — catch full disk before the runner goes offline.
- Add safety-net cron for daily `docker system prune -af --filter "until=48h"`.
- Cap journald disk usage: `SystemMaxUse=500M` in `/etc/systemd/journald.conf.d/size-limit.conf`.
- To replace a runner: use `infra/github-runner/replace-runner.sh`.
- Check IAM role has `CloudWatchAgentServerPolicy` attached before launching.
