# PRIMARY MAIN R212 — M1-002 required PR creation blocked

generation_id: MAIN-20260930T221715+0900-PRIMARY-R212-R175-R140-M1-002-PR-CREATE-BLOCKED
generated_at: 2026-09-30T22:17:15+09:00
role: PRIMARY_MAIN
mode: SYSTEM_BUILD
build_id: BUILD-SB-M1-002-INTEGRATED-ROBUSTNESS-HARNESS
new_scientific_result: false
scientific_credit: 0

## Freshness and authority

Current main policy was re-fetched from main at `59fc994b39d0ba02682e972161bb46801592d25b`: AGENTS.md, COMMON.md, SCIENTIFIC_INTEGRITY.md, ACTIVE_POLICY.md and MAIN.md. Repository procedures for SYSTEM_BUILD, FORMAL integrity boundary, persistence and P0 diagnosis were also re-fetched from main.

Human Directive freshness handshake resolved `ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d` with active-index blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`. This matches durable MAIN R211; directive delta is false.

Durable Evidence Analyst authority is R175 at `ops/evidence-analyst-handoff@0dc403147643caff4f6955a3e41edd9b9bf2d8b4`. R175 retains `M1_002_EXACT_HEAD_PR_CONDITIONAL_MERGE` authority and records Relay unallocated. Current append-only Control authority is R140 at `ops/control-brain-handoff@b067a505b8e800196173bceaeafffd5afc0926ea`; moving Control latest/state remain R139 and are cache debt only. Prior durable MAIN is R211 at `ops/orchestrator-run-report@f1d683b72c3f79a273b5c7264f4d01a2e69fd6ba`, with R211 history/latest/state/lease aligned before this publication.

## M1-002 exact state

Working branch: `system-build/m1-post-integration-robustness-20260928`
Exact head: `2a21d3e879f1db4e81a58273180ad2124e823a5e`
Base main: `59fc994b39d0ba02682e972161bb46801592d25b`
Fresh compare: 1 ahead / 0 behind.
CI: run `36361950457`, completed/success on Python 3.11 and 3.13; Install, Lint, Local readiness, Test and Validate bundle all succeeded.
Fresh PR readback before execution: none.

## Required PR creation

Under R175 exact-head authority, the required PR-create purpose was attempted five total times. Before every retry, main head, candidate head and PR absence were re-read.

All five `create_pull_request` invocations were refused before GitHub with the observed platform message: `This tool call was blocked by OpenAI's safety checks. Please double check what you are sending.`

Final independent readback still showed zero matching PRs, unchanged main and candidate heads, and no merge. Failure layer: `PRE_GITHUB_PLATFORM_SAFETY_REFUSAL`. Attempt count: 5/5.

P0 `INC-GITHUB-MUTATION-RECURRENCE-20260928-001` remains OPEN; root cause UNKNOWN; current bounded classification remains `PERSISTENT_CREATE_PULL_REQUEST_PRE_GITHUB_REFUSAL_WITH_NONUNIFORM_INTERMITTENT_OTHER_MUTATIONS`. This current-run failure does not suspend the recurring scheduler.

## SYSTEM_BUILD classification

- built: true
- bounded functionally verified: true
- comparatively supported: false
- composition contribution: NOT_ESTABLISHED
- scientifically novel: false
- scientific credit: 0
- evidentiary status: NON_EVIDENTIARY_BUILD
- SB003: ALLOCATED_CONDITIONAL_INACTIVE
- Relay: unallocated / no collision observed

No FORMAL execution, scientific rerun/retune/rescore/redispatch, immutable-evidence mutation, terminal reopen, scheduler state change, or Work/Work-backed execution occurred.

Stop reason: `PR_CREATION_BLOCKED_AFTER_5_MUTATION_ATTEMPTS`.
Next action: re-fetch authority/exact state on the next run and retry the required PR-create purpose only if still authorized.
