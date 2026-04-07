# Wiki Eval: Does institutional knowledge beat code reading?

## How to run

For each question, run two fresh Claude Code sessions in the field1st repo:

**Session A (wiki disabled):**
> "Ignore ~/.claude/wiki/ completely. Do NOT read any wiki files. Answer from the codebase only: [QUESTION]"

**Session B (wiki enabled):**
> "[QUESTION]"

Score each answer:
- **Correct** — factually right, actionable
- **Partial** — some right, missing key context
- **Wrong/Missing** — couldn't answer or got it wrong

The wiki wins if Session B answers questions that Session A can't.

---

## The 10 Questions

### Q1: Why do we override WAF rules to COUNT instead of disabling them?
**What the code shows:** Terraform with `rule_action_override { count {} }` and a reblock rule.
**What only the wiki knows:** The trade-off reasoning — disabling loses the label, COUNT preserves the label so we can selectively re-block on non-upload paths. This was a deliberate architectural choice, not the obvious path. Also: James found the original conditional was *inverted* (PR #264), meaning all 9 prod tenants had no WAF at all.
**Wiki entries:** enable-waf-production, waf-upload-path-exemptions, waf-genericlfi-body

### Q2: What happens if you pass an HTTPS signed URL to Vertex AI instead of fetching the image server-side?
**What the code shows:** `fetchImageAsBase64()` call with inlineData.
**What only the wiki knows:** The failure mode — signed URLs expire between our server receiving the request and Vertex processing it. 29 errors in one day. The original `clearTimeout` was in `.then()` instead of `finally`, so the timeout didn't cover body download.
**Wiki entries:** vertex-server-side-image-fetch

### Q3: We need to add offline support for a new mobile feature. What's the established pattern?
**What the code shows:** Various offline implementations scattered across files.
**What only the wiki knows:** The complete pattern: offlineActionQueue → negative temp IDs for placeholders → sync status icons (pending/syncing/success/failed) → discriminated union result types → concurrency locks → filesystem for binary data (not AsyncStorage). Plus: VLM scan established it, doc-from-hazard replicated it, Voice1st adapted it. And the gotchas: iOS picker hide/show dance causes unresponsive buttons, duplicate useAsyncEffect hooks cause race conditions.
**Wiki entries:** vlm-offline-scan, offline-doc-from-hazard, voice1st-offline-save, offline-hazard-assessment, airplane-mode-recovery

### Q4: Why does the mobile app treat `isInternetReachable === null` as online instead of offline?
**What the code shows:** A conditional check in the connection reducer.
**What only the wiki knows:** The root cause — treating null as offline delayed the offline→online transition by up to 60 seconds because null is a transient "checking" state, not a definitive "offline" state. This was one of seven cascading failures that caused the app to freeze after airplane mode toggle. The fix was part of a larger cascade: fetch timeout + timestamp locks + null handling + duplicate effect consolidation.
**Wiki entries:** airplane-mode-detection, airplane-mode-recovery

### Q5: Thomas switched the PDF extraction from Vercel AI SDK to Google GenAI SDK. Why?
**What the code shows:** Current code uses `createInstrumentedVertexClient`.
**What only the wiki knows:** Vercel AI SDK created the Vertex client at module import time, before `ensureGoogleCredsFile()` materialized credentials. The fix wasn't about the SDK being bad — it was about *when* the client was created. The Google GenAI SDK gives explicit control over initialization timing.
**Wiki entries:** pdf-extraction-vertex-credentials

### Q6: A developer wants to add explicit yxyx coordinate instructions to the Gemini hazard prompt. Should they?
**What the code shows:** Gemini workflow passes `includeCoordinateFormat: false`.
**What only the wiki knows:** This was tried and DEGRADED quality. Gemini's bounding box detection is native — it always returns yxyx regardless of prompt text. Adding explicit instructions confused the model: Vault1 went from 9 diverse hazards to 10 identical bounding boxes. The fix was to split the prompt: explicit instructions for Bedrock/OpenAI, neutral instructions for Gemini.
**Wiki entries:** bbox-yxyx-standardization

### Q7: Our Chat V2 guardrails are blocking a user who asked "What is the hazard of confined space entry?" Is this expected?
**What the code shows:** The guardrails prompt with allow/block rules.
**What only the wiki knows:** This exact false positive was the motivation for PR #150. The guardrails were over-indexed on danger keywords. The fix was a decision priority rubric: first check if the message is about safety assessment (allow), then check for wrongdoing (block). Danger words like "confined space" and "explosion" are expected in legitimate safety work.
**Wiki entries:** guardrails-allow-hazard-queries

### Q8: How should image size limits work when sending images to Bedrock via Converse API?
**What the code shows:** A `MAX_INLINE_IMAGE_BYTES` constant and compression logic.
**What only the wiki knows:** A 5.03MB JPEG was rejected as 6.7MB because Converse API adds ~1.7MB encoding overhead. The threshold was lowered from 5MB to 3.75MB. Also: JPEG quality compression (75%) preserves resolution better than dimension resize for bounding box accuracy — this was a deliberate choice when unifying Bedrock on Converse API.
**Wiki entries:** hazard-eval-compression, bedrock-converse-unification

### Q9: James added HTTP security headers. Why was CSP omitted from the AI orchestration service?
**What the code shows:** Hono `secureHeaders()` middleware without CSP.
**What only the wiki knows:** The AI orchestration service is a pure JSON API — it never serves HTML. CSP only protects HTML documents from executing injected scripts. Adding CSP to a JSON API would be security theater. Other headers (X-Frame-Options, HSTS, X-Content-Type-Options) still apply because they protect against framing and protocol downgrade.
**Wiki entries:** http-security-headers

### Q10: The self-hosted GitHub Actions runner went offline. What's the most likely cause and how do we fix it?
**What the code shows:** A cleanup hook script and CloudWatch config.
**What only the wiki knows:** The runner went offline after 36 days because the 50GB disk filled from Docker images (~30GB), Gradle caches (~10GB), and runner _work/ directories (~5GB). SSM commands silently fail when disk is full — you can't even diagnose remotely. The fix was a post-job cleanup hook (ACTIONS_RUNNER_HOOK_JOB_COMPLETED), CloudWatch monitoring, and a replace-runner.sh script. Also: `docker image prune -a` is too aggressive — use `--filter "until=24h"`.
**Wiki entries:** github-runner-auto-cleanup

---

## Scoring rubric

| Score | Wiki disabled | Wiki enabled | Verdict |
|-------|--------------|-------------|---------|
| 10/10 both | Wiki adds nothing | Wiki adds nothing | Wiki not needed for these questions |
| Wiki < 5, Code < 5 | Neither can answer well | Neither can answer well | Questions are too hard / knowledge is lost |
| Wiki > 7, Code < 4 | Code can't answer | Wiki nails it | **Wiki proves its value** |
| Wiki > 7, Code > 7 | Both answer well | Both answer well | Wiki is redundant for these questions |

**Target: Wiki > 7, Code < 4 on at least 7/10 questions.**

If we hit that, the wiki is delivering knowledge the codebase alone can't provide. That's the foundation everything else builds on.
