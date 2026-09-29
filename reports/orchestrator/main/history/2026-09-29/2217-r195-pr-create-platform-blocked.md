# PRIMARY MAIN R195 — M1-002 required PR creation blocked

generation_id: `MAIN-20260929T221719+0900-PRIMARY-R195-M1-002-PR-CREATE-BLOCKED`
generated_at: `2026-09-29T22:17:19+09:00`
mode: `SYSTEM_BUILD`

Human Directive freshness handshake completed against `ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d`, active-index blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`; no directive delta versus durable R194. Applicable directives read: HUMAN-20260925-002, HUMAN-20260926-003, HUMAN-20260926-004, HUMAN-20260927-002, HUMAN-20260928-001, HUMAN-20260928-002.

Evidence Analyst durable authority remains R170 at `cebf72d66ee5d0c9ef27395af847f58799e99bcb`, retaining `RETAIN_EXACT_HEAD_PR_CONDITIONAL_MERGE` for M1-002. Control append-only durable authority advanced to R126; its latest/state moving caches still expose R125, so R126 history is treated as authority. P0 `INC-GITHUB-MUTATION-RECURRENCE-20260928-001` remains OPEN / root cause UNKNOWN.

M1-002 exact branch `system-build/m1-post-integration-robustness-20260928` remains at `2a21d3e879f1db4e81a58273180ad2124e823a5e`, 1 ahead / 0 behind `main@59fc994b39d0ba02682e972161bb46801592d25b`. Push CI run `36361950457` remains completed/success. Current Analyst allocation has relay=null; no conflicting PR exists.

The required PR-create purpose was attempted five total times. Before every retry the exact candidate head, current main head, and PR absence were re-read. Attempts 1-5 were all refused before GitHub with: `This tool call was blocked by OpenAI's safety checks. Please double check what you are sending.` Independent readback after each completed attempt showed zero matching open PRs. Merge was not attempted.

Failure layer: `PRE_GITHUB_PLATFORM_SAFETY_REFUSAL`.
P0 classification remains consistent with a nonuniform/intermittent pre-GitHub mutation refusal, with `create_pull_request` the strongest recurring surface. Control R126 independently reproduced the same five-of-five refusal on an isolated non-scientific PR canary.

Build classification: built=true; bounded_functionally_verified=true; comparatively_supported=false; composition_contribution=NOT_ESTABLISHED; scientifically_novel=false; scientific_credit=0; evidentiary_status=NON_EVIDENTIARY_BUILD.

No scientific experiment, FORMAL execution, immutable evidence, consumed identity, scheduler state, cadence, or Work-backed execution was changed.

stop_reason: `PR_CREATION_BLOCKED_AFTER_5_MUTATION_ATTEMPTS`
next_action: `REFETCH_AND_RETRY_IF_STILL_AUTHORIZED`
