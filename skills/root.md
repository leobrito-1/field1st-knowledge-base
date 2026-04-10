# Wiki-First Retrieval

## What this does

Before answering questions about the codebase, the LLM checks the wiki first.

The wiki is a pre-indexed knowledge graph built from structured entries (`raw/`). Each entry captures a decision, a bug fix, or a pattern — written by humans, in plain language, with frontmatter metadata that makes it searchable.

## Why this matters

Code tells you **what** exists. Git tells you **when** it changed. Neither tells you **why** a decision was made, what was tried and failed, or what breaks if you change it.

An LLM reading source code to answer "why did we do X?" has to:
1. Find the relevant files (search across the whole repo)
2. Read them (burn tokens on implementation details)
3. Infer intent from code structure (guess, basically)

The wiki short-circuits this. The entry already contains the problem, the trade-offs, and the lessons — indexed by tags, answers (searchable symptoms), and related entries. The LLM reads one file instead of twenty.

**Fewer tokens. Better answers. No guessing.**

## How to wire it up

Add this to your `CLAUDE.md` (or equivalent LLM instruction file):

```markdown
Before answering questions about architecture, past decisions, bugs, or patterns:

1. Read `<wiki-dir>/graphify-out/wiki/index.md` — it maps all knowledge by community.
2. Follow links to relevant community articles.
3. Read the specific raw entries referenced in those articles.
4. Answer using wiki context first. Only read source code if the wiki doesn't cover it.
```

If no graph exists yet, fall back to searching `raw/` by frontmatter tags and `answers` fields.

## The loop

```
code change → /wiki captures the knowledge → /graphify indexes it → LLM reads the index → better answers
```

Three skills make this work:

| Skill | Purpose |
|-------|---------|
| `/wiki` | Captures knowledge from coding sessions into `raw/` entries |
| `/graphify` | Builds a knowledge graph from `raw/` — communities, connections, search index |
| This file | Tells the LLM to check the graph before reading code |

## When to check the wiki

- Architecture questions ("how does offline sync work?")
- Past decisions ("why did we use X instead of Y?")
- Bug patterns ("we've seen this before")
- Cross-system interactions ("what happens when WAF meets image uploads?")

## When to skip the wiki

- The question is about current code state (read the code)
- The question is about recent git history (run git log)
- The entry is old and the code has changed (verify before trusting)
