# PRIMARY MAIN R216 — M1-002 PR #164 merge blocked after exact-head CI success

generation_id: MAIN-20261001T081133+0900-PRIMARY-R216-R176-R143-M1-002-PR164-MERGE-BLOCKED
generated_at: 2026-10-01T08:11:33+09:00
role: PRIMARY_MAIN
mode: SYSTEM_BUILD
build_id: BUILD-SB-M1-002-INTEGRATED-ROBUSTNESS-HARNESS
new_scientific_result: false

Human Directive freshness handshake: ops/human-directives head `8ce979b9ec0bc7eede5225c0403698f8886d3e8d`; active-index blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`; no delta from durable MAIN R215. Applicable active directives read: HUMAN-20260925-002, HUMAN-20260926-003, HUMAN-20260926-004, HUMAN-20260927-002, HUMAN-20260928-001.

Evidence Analyst authority remains R176 at `acf01924d3db1fef0cbba3565db8aba2433ab642`; M1-002 allocation remains exact-head PR/conditional-merge authority for `2a21d3e879f1db4e81a58273180ad2124e823a5e`. Relay remains unallocated; fresh MAIN lease before action was R215 / WAITING_EXTERNAL_PR_CI, so no Relay collision was observed. Control durable append-only authority remains R143 at `2b13447570e203b3efccdc5ded9ecd5bd0503d05`.

M1-002 live state: branch `system-build/m1-post-integration-robustness-20260928`, exact head `2a21d3e879f1db4e81a58273180ad2124e823a5e`; current main `59fc994b39d0ba02682e972161bb46801592d25b`; 1 ahead / 0 behind. PR #164 is open, non-draft and mergeable=true. Pull-request CI run `36778206722` is completed/success on the exact head; Python 3.11 and 3.13 jobs both passed Install, Lint, Local readiness, Test and Validate bundle.

MAIN attempted the authorized conditional merge five times with `expected_head_sha=2a21d3e879f1db4e81a58273180ad2124e823a5e`. Before each retry the live PR/base/head and Analyst authority were re-fetched. All five attempts were refused before GitHub with the observed platform message. Final readback shows PR #164 still open/unmerged, exact head unchanged, main unchanged and CI still green. Failure layer: `PRE_GITHUB_PLATFORM_SAFETY_REFUSAL`. No direct-main bypass was used.

P0 `INC-GITHUB-MUTATION-RECURRENCE-20260928-001` remains OPEN / root cause UNKNOWN. Read paths remained healthy. SYSTEM_BUILD classification remains built=true; bounded_functionally_verified=true; comparatively_supported=false; composition_contribution=NOT_ESTABLISHED; scientifically_novel=false; scientific_credit=0; NON_EVIDENTIARY_BUILD. No FORMAL/scientific execution or scheduler-state change occurred.

stop_reason: PR164_MERGE_BLOCKED_AFTER_5_PRE_GITHUB_REFUSALS
next_action: Re-fetch current directive identity, Analyst authority, MAIN/Relay collision state, main/candidate/PR/CI and retry the exact-head conditional merge on the next MAIN run only if the same conditions still hold.
