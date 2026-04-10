# Knowledge Base

A structured wiki that gives LLMs institutional memory. Instead of reading your entire codebase to answer "why did we do X?", the LLM reads a pre-indexed knowledge graph built from short, human-written entries.

**The problem it solves:** Code shows what exists. Git shows when it changed. Neither shows why a decision was made, what failed before the fix, or what breaks if you touch it. LLMs guess. This wiki replaces guessing with indexed recall.

## How it works

```
coding session
  → /wiki captures the decision as a raw entry
  → /graphify builds a knowledge graph from all entries
  → LLM checks the graph before reading source code
  → fewer tokens, better answers, no re-discovery
```

Three skills run the loop:

| Skill | What it does |
|-------|-------------|
| `skills/root.md` | Instructs the LLM to check the wiki before answering — the retrieval pattern |
| `skills/wiki/` | Captures knowledge from coding sessions into structured `raw/` entries |
| `skills/graphify/` | Turns `raw/` into a navigable knowledge graph with community detection |

## Repo structure

```
raw/                   # knowledge entries — the source of truth
skills/
  root.md              # wiki-first retrieval instruction
  wiki/SKILL.md        # entry capture skill
  graphify/SKILL.md    # graph pipeline skill
schema.yaml            # entry validation contract
tags.yaml              # canonical tag list with aliases
validate.py            # lints entries against the schema
health.py              # checks filename policy, log consistency, graph staleness
```

## Knowledge unit

Each unit in `raw/` is a markdown file with YAML frontmatter:

```markdown
---
project: my-project
repo: org/my-project
date: 2026-04-01
author: jane.doe
tags: [offline, react-native]
answers: ["App freezes after airplane mode toggle", "Offline sync stuck on pending"]
files: [src/sync/queue.ts, src/hooks/useConnection.ts]
---

# Airplane mode recovery cascade

## The problem
What was going wrong, in plain language.

## What we did
The solution, factually.

## Why this way and not another
The trade-off. What alternatives existed.

## What we learned
Takeaways that apply beyond this specific change.

## Technical reference
File paths, commands, implementation details.
```

The `answers` field is key — it contains symptoms and error messages someone would search for. The graph indexes these so the LLM can match a problem to an entry without scanning the codebase.

## Getting started

**To use this as a template:**

1. Fork the repo
2. Delete the entries in `raw/` (they're specific to our project)
3. Edit `tags.yaml` with your project's domain tags
4. Wire up the retrieval instruction from `skills/root.md` into your LLM config (e.g., `CLAUDE.md`)
5. Start capturing: after meaningful PRs, run the wiki skill to create entries
6. Build the graph: run `/graphify raw/` to generate the knowledge graph

**To build the graph from existing entries:**

```bash
pip install graphifyy
# Then invoke /graphify raw/ in your LLM coding tool
```

The graph outputs to `graphify-out/` (gitignored). It contains an interactive HTML visualization, a JSON graph for programmatic access, and community-clustered wiki articles.

## Open problems

This system works but has real limitations. They're unsolved.

**Staleness.** Entries describe the codebase at a point in time. Code changes. The entry about "how offline sync works" might be wrong six months later if someone refactored the queue. The `files` frontmatter field exists for staleness detection — if those files change significantly, the entry needs review. `health.py` can flag stale entries, but doesn't fix them.

**Linting burden.** Every entry needs to pass schema validation, use canonical tags, follow the section template, and contain searchable `answers`. This friction is intentional (it keeps quality high) but it means entries don't write themselves. The `/wiki` skill automates most of this, but someone still has to review and approve.

**No self-healing.** When an entry becomes stale, nothing happens automatically. The ideal system would detect that referenced files changed, diff the entry against current code, and either update the entry or flag it for human review. This doesn't exist yet. The `files` field and `health.py` are the scaffolding for it, but the actual reconciliation loop is unbuilt.

**Graph drift.** The knowledge graph in `graphify-out/` is derived from `raw/`. If you add entries and forget to rebuild, the graph is stale. The `/wiki` skill triggers a rebuild automatically after each capture, but manual edits to `raw/` won't trigger anything.

## Validation

```bash
# Validate a single entry
python3 validate.py raw/2026-04-01-my-entry.md

# Run full health check (filename policy, schema, consistency, staleness)
python3 health.py
```

## License

MIT
