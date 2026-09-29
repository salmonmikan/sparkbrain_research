# PRIMARY MAIN R189 — M1-002 PR creation blocked in current run

generation_id: MAIN-20260929T131547+0900-PRIMARY-R189-M1-002-PR-CREATE-BLOCKED
generated_at: 2026-09-29T13:15:47+09:00
role: PRIMARY_MAIN
mode: SYSTEM_BUILD
build_id: BUILD-SB-M1-002-INTEGRATED-ROBUSTNESS-HARNESS
new_build_result: false
new_scientific_result: false

## Authority and freshness

Main scheduler policy was re-fetched explicitly from `main@59fc994b39d0ba02682e972161bb46801592d25b`.
Human Directive index remains `ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d` with active-index blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`; this matches durable Analyst R169, so directive delta is false.

Durable Evidence Analyst authority is R169 at `95972cb31cb26d5994e506bfa46e6a11dc786a15`.
Current durable Control authority is append-only R120 at `9e4e029b65957c866765baa67af1634727bf2922`.
Durable MAIN authority before this generation is R188 at `d22df96223246c20748a1e2480f576d92e40061b`.
Relay is not allocated and no relay branch/collision is observed.

## Exact build state

- exact branch: `system-build/m1-post-integration-robustness-20260928`
- exact head: `2a21d3e879f1db4e81a58273180ad2124e823a5e`
- base main: `59fc994b39d0ba02682e972161bb46801592d25b`
- divergence: 1 ahead / 0 behind
- CI run: `36361950457`
- CI status: completed / success
- matching open PR after final readback: none

R169 exact-head PR / conditional-merge authority remains valid. M1-002 remains built and bounded-functionally verified only. Comparative support is false, composition contribution is NOT_ESTABLISHED, scientific novelty is false, and scientific credit is 0.

## Current-run PR creation attempts

The authorized five-total-attempt ceiling was consumed for the PR-creation purpose.

Attempt 1 entered the Code Mode orchestration but the wrapper exceeded its tool-call ceiling before the mutation result could be captured. Independent readback found no PR, so no stronger failure-layer claim is made for attempt 1.

Attempts 2 through 5 each re-fetched current Analyst/main/build/PR state before retry. All four explicit `create_pull_request` calls were refused before GitHub with:

`This tool call was blocked by OpenAI's safety checks. Please double check what you are sending.`

PR payloads were progressively shortened through the retries, including a final attempt with title/head/base only. Final independent readback still found no matching open PR. No merge was attempted.

## P0 disposition

`INC-GITHUB-MUTATION-RECURRENCE-20260928-001` remains OPEN with root cause UNKNOWN.
The exact observed failure layer for attempts 2-5 is `PRE_GITHUB_PLATFORM_SAFETY_REFUSAL`.
Control R120 independently reports the same PR-create failure on isolated canary refs, further bounding the issue away from the production branch payload alone.
Repository-wide write outage remains unsupported.

## Claim boundary and next action

- built: true
- bounded functionally verified: true
- comparatively supported: false
- composition contribution: NOT_ESTABLISHED
- scientifically novel: false
- scientific credit: 0
- evidentiary status: NON_EVIDENTIARY_BUILD
- SB003: ALLOCATED_CONDITIONAL_INACTIVE
- science execution: none
- next action: re-fetch authority/head/PR state on next run and retry exact-head PR creation only if still authorized
