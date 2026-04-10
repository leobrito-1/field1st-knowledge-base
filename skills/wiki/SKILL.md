---
name: wiki
description: "Capture structured knowledge from Claude Code sessions into the current repo's .wiki/ directory (fallback ~/.claude/wiki/). Triggered after /pr or invoked standalone."
argument-hint: "[review | capture | update | optional: extra context]"
---

# Wiki Knowledge Capture

Extract and persist structured knowledge from this session.

## Task

$ARGUMENTS

## Canonical path

Resolve `WIKI_DIR` before doing anything else:

- If `git rev-parse --show-toplevel` succeeds and `<repo-root>/.wiki/` exists, use that as canonical.
- Otherwise, fall back to `~/.claude/wiki/`.

All paths below refer to `WIKI_DIR`.

## Modes

Determine mode from arguments:
- No arguments or invoked by `/pr` → **Entry creation** (PR context available)
- `capture` → **Capture mode** (no PR required — for bug hunts, spikes, experiments)
- `update` → **Update mode** (refresh derived artifacts from the current raw corpus)
- `review` → **Draft review** (process pending drafts)

---

## Mode: Entry Creation

### 1 — Gather context (parallel)

```bash
git rev-parse --abbrev-ref HEAD
git log --oneline develop..HEAD 2>/dev/null || git log --oneline main..HEAD
git diff --stat develop...HEAD 2>/dev/null || git diff --stat main...HEAD
git remote get-url origin 2>/dev/null
git config user.name 2>/dev/null
```

Also check:
- **Branch name** — extract Jira key if present (pattern: `[A-Z][A-Z0-9]+-\d+`)
- **Plan file** — check `.plans/<branch-name>.md` (replace `/` with `-`)
- **PR context** — if invoked by `/pr`, the PR number, URL, Jira key, and repo name are already in conversation context

### 2 — Triage

Before drafting, assess whether this PR produced knowledge worth capturing.

**Worth capturing:**
- Non-obvious root cause discovered
- Architectural decision with trade-offs considered
- New pattern established or existing pattern learned
- Friction/debugging that would save someone else time
- Cross-system interaction or surprising behavior
- Environment/tooling knowledge (Docker quirks, WAF behavior, etc.)

**Skip:**
- Straightforward cosmetic/UI tweaks with no surprises
- Simple config changes with no gotchas
- Obvious bug fixes where the fix IS the lesson
- Dependency bumps with no behavioral impact
- Typo/formatting fixes

If the PR is low-value, recommend skipping:
> "This was a straightforward [description] — no significant lessons or decisions to capture. Skip wiki entry? (yes/no)"

If the user says no and explains what was valuable, proceed to drafting with that guidance. If yes, report "Wiki entry skipped." and exit.

### 3 — Read the diff

```bash
git diff develop...HEAD 2>/dev/null || git diff main...HEAD
```

Read the plan file if it exists. Read recent commit messages. These are your primary sources for the entry.

### 4 — Read canonical tags

```bash
cat <WIKI_DIR>/tags.yaml
```

When generating tags in step 5, fuzzy-match each tag against this canonical list. If a near-match exists (e.g., you'd generate `cloud-front` but `cloudfront` exists as canonical), use the canonical form. If no match, use the new tag as-is.

### 5 — Draft the entry

Using full session context (conversation history, diff, plan file, commits), write a wiki entry following this exact template. PRs that fix multiple bugs are kept as a single entry — Graphify handles discoverability of individual concepts via its graph.

```markdown
---
project: <inferred from repo name — e.g., "field1st" from "leonardobrito/field1st">
repo: <from git remote>
jira: <from branch name, or omit if none>
pr: <PR number, from conversation context>
branch: <current branch>
date: <today, YYYY-MM-DD>
author: <from git config user.name, mapped to short form>
packages: [<inferred from changed files — which packages/ dirs were touched>]
tags: [<3-6 canonical tags describing the domain and technology>]
related: [<filename stems of related entries if any exist in <WIKI_DIR>/raw/>]
answers: ["<3-5 symptoms or error messages someone would search for>"]
files: [<key source files changed — max 5, for staleness detection>]
---

# <Title — what this is about, plain language>

## The problem
<What was going wrong, in plain language. A non-technical person
should understand why this mattered. 2-4 sentences.>

## What we tried that didn't work
<The approach that failed, and why. This is the most valuable
section — it prevents the next person from trying the same thing.
Skip this section entirely if the first approach worked.>

## What we did
<The solution, factually. What changed and how it works.
1-3 sentences.>

## Why this way and not another
<The trade-off. What alternatives existed and why this was better.
Bullet points preferred.>

## What we learned
<Takeaways that apply beyond this specific change. Each bullet
stands alone — you don't need the rest of the entry to understand
it. If nothing was genuinely surprising, one honest sentence.>

## Technical reference
<File paths, commands, implementation details, and concrete next-touch
guidance. This section is for the developer who needs to touch this code next.>
```

### 6 — Quality self-check

Before presenting the draft, validate against these criteria. If any check fails, rewrite the failing section before continuing.

| Check | Criteria |
|-------|----------|
| The problem | Would a non-technical person understand what was going wrong and why it mattered? No unexplained jargon? |
| What we tried that didn't work | Does it name the specific approach that failed and explain why? Would it prevent someone from repeating the mistake? If nothing failed, is this section omitted (not padded)? |
| What we did | Factual, concise, no diff-speak? Could you explain it to a colleague in one breath? |
| Why this way and not another | Does it name at least one alternative that was considered? Clear on why this path won? |
| What we learned | Each bullet stands alone? Applies beyond this specific change? No invented wisdom — if nothing surprising, one honest sentence? |
| Technical reference | Has specific file paths, commands, or config references? Developer can act on it? |
| Plain language | Could a PM or new hire read the first 4 sections and understand the story? No jargon without explanation? |
| answers: | Phrased as symptoms or error messages someone would search for? Not conceptual? |
| tags: | All fuzzy-matched against tags.yaml? No synonyms of existing canonical tags? |
| No padding | Every sentence carries information? No filler? |

### 7 — Schema validation gate

Write the draft to a temp file and validate:

```bash
python3 <WIKI_DIR>/validate.py /tmp/wiki-draft.md
```

If validation fails, fix the errors and re-validate. Do not present to the user until validation passes.

### 8 — Present for review

Show the full entry to the user. Ask: **approve**, **edit**, **later**, or **skip**.

- **Approve** (or "looks good", "yes", "lgtm", etc.):
  1. Write to `<WIKI_DIR>/raw/<date>-<short-description>.md`
     - Filename: always `YYYY-MM-DD-short-description.md` — lowercase, hyphens, no spaces, no author prefix. E.g., `2026-04-07-waf-body-rules-count-mode.md`
  2. Append to `<WIKI_DIR>/log.md`:
     ```
     ## [<date>] pr | <jira-key-or-none> | <title>
     - Project: <project>
     - PR: #<number>
     - Entry: [raw/<filename>]
     ```
  3. If `<WIKI_DIR>/graphify-out/` already exists, run a best-effort local refresh by invoking:
     ```text
     /graphify <WIKI_DIR>/raw --update
     ```
     - This is maintenance, not a user decision point. Do it automatically after save.
     - If it fails, do **not** roll back the saved entry. Continue and report that the graph may be stale.
  4. Run hidden wiki maintenance:
     ```bash
     python3 <WIKI_DIR>/health.py
     ```
     - If it reports warnings only, keep going and summarize them briefly.
     - If it reports errors, keep the saved entry and surface the errors after the save completes.
  5. Report: "Wiki entry saved to `<WIKI_DIR>/raw/<filename>`"
     - If graph refresh succeeded, mention that `graphify-out/` was refreshed.
     - If graph refresh failed or health found issues, mention those after the save confirmation.

- **Edit**: User gives feedback. Revise the draft, re-run quality self-check (step 6) and schema validation (step 7), re-present.

- **Later**: Write to `<WIKI_DIR>/drafts/<filename>` instead. Report: "Draft saved to `<WIKI_DIR>/drafts/<filename>`. Run `/wiki review` to process later."

- **Skip**: Write nothing. Report: "Wiki entry skipped."

---

## Mode: Capture

Same as Entry Creation, but:
- No PR context needed — `pr` and `branch` fields are optional
- Gather context from conversation history only (no diff)
- Same triage step applies — if the session produced nothing worth capturing, recommend skipping
- Use `--mode capture` flag for schema validation:
  ```bash
  python3 <WIKI_DIR>/validate.py /tmp/wiki-draft.md --mode capture
  ```
- Log entry uses `capture` type instead of `pr`:
  ```
  ## [<date>] capture | <jira-key-or-none> | <title>
  - Project: <project>
  - Entry: [raw/<filename>]
  ```

---

## Mode: Draft Review

### 1 — List pending drafts

```bash
ls <WIKI_DIR>/drafts/*.md 2>/dev/null
```

If no drafts exist, report "No pending drafts." and exit.

### 2 — Process each draft

For each draft:
1. Read and present the content
2. Ask: **approve**, **edit**, or **delete**
   - **Approve**: Move to `<WIKI_DIR>/raw/`, append to log
   - **Edit**: User gives feedback, revise, re-validate, re-present
   - **Delete**: Remove the draft file

---

## Mode: Update

Refresh the derived wiki artifacts so the user does not need to think about `/graphify` directly.

### 1 — Decide refresh path

- If `<WIKI_DIR>/graphify-out/graph.json` exists, invoke:
  ```text
  /graphify <WIKI_DIR>/raw --update
  ```
- If no graph exists yet, invoke:
  ```text
  /graphify <WIKI_DIR>/raw
  ```

### 2 — Run hidden maintenance after refresh

```bash
python3 <WIKI_DIR>/health.py
```

### 3 — Report concisely

- If refresh succeeds and health passes: report that the wiki graph was updated.
- If refresh succeeds with health warnings: report that the wiki graph was updated and summarize the warnings briefly.
- If refresh fails: report that raw entries are unchanged and the graph may be stale.

---

## Rules

- **Never skip the quality self-check** — it's what prevents entries from becoming noise
- **Never skip schema validation** — it's the structural guarantee
- **Always present before writing** — the user reviews every entry
- **Use plain date-based filenames** — always `YYYY-MM-DD-short-description.md`; never encode the author in the filename
- **Refresh derived artifacts automatically** — after approve, invoke `/graphify <WIKI_DIR>/raw --update` when `graphify-out/` already exists
- **Run hidden wiki maintenance after save** — `python3 <WIKI_DIR>/health.py` should happen automatically; only surface actionable issues
- **Additive only** — this skill never modifies existing entries in `raw/`
- **Degrade gracefully** — if context is thin (e.g., backfilling an old PR), write what you can and be honest about gaps. One honest sentence beats three guessed ones.
- **No filler, ever** — if a section has nothing meaningful, write one sentence that says so plainly. Don't pad.
