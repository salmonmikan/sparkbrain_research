# PRIMARY MAIN R217 — M1-002 PR #164 merge remains blocked after exact-head CI success

generation_id: MAIN-20261001T091641+0900-PRIMARY-R217-R176-R143-M1-002-PR164-MERGE-BLOCKED
generated_at: 2026-10-01T09:16:41+09:00
role: PRIMARY_MAIN
mode: SYSTEM_BUILD
build_id: BUILD-SB-M1-002-INTEGRATED-ROBUSTNESS-HARNESS
new_scientific_result: false

Human Directive freshness handshake: ops/human-directives head `8ce979b9ec0bc7eede5225c0403698f8886d3e8d`; active-index blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`; no delta from durable MAIN R216. Applicable active directives read: HUMAN-20260925-002, HUMAN-20260926-003, HUMAN-20260926-004, HUMAN-20260927-002, HUMAN-20260928-001.

Evidence Analyst authority remains R176 at `acf01924d3db1fef0cbba3565db8aba2433ab642`; M1-002 allocation remains exact-head PR/conditional-merge authority for `2a21d3e879f1db4e81a58273180ad2124e823a5e`. Relay allocation remains null. Control durable append-only authority remains R143 at `2b13447570e203b3efccdc5ded9ecd5bd0503d05`.

Live state: main `59fc994b39d0ba02682e972161bb46801592d25b`; M1-002 exact head `2a21d3e879f1db4e81a58273180ad2124e823a5e`; compare 1 ahead / 0 behind. PR #164 is open, non-draft and mergeable=true. Pull-request CI run `36778206722` is completed/success on the exact head; Python 3.11 and 3.13 jobs both passed Install, Lint, Local readiness, Test and Validate bundle.

MAIN attempted the authorized conditional merge five total times with `expected_head_sha=2a21d3e879f1db4e81a58273180ad2124e823a5e`. Before every retry, PR/base/head and Analyst authority were freshly re-read. Attempt 1 returned a tool error whose message was not captured by that call; independent readback showed no GitHub state change. Attempts 2-5 explicitly returned `This tool call was blocked by OpenAI's safety checks. Please double check what you are sending.` Final readback shows PR #164 still open/unmerged, exact head unchanged and main unchanged. No direct-main bypass was used.

P0 `INC-GITHUB-MUTATION-RECURRENCE-20260928-001` remains OPEN / root cause UNKNOWN. SYSTEM_BUILD classification remains built=true; bounded_functionally_verified=true; comparatively_supported=false; composition_contribution=NOT_ESTABLISHED; scientifically_novel=false; scientific_credit=0; NON_EVIDENTIARY_BUILD. No FORMAL/scientific execution or scheduler-state change occurred.

Before this publication, append-only MAIN authority was R216 while latest/state/lease were R215, so pointer debt existed.

stop_reason: PR164_MERGE_BLOCKED_AFTER_5_ATTEMPTS_WITH_4_EXPLICIT_PRE_GITHUB_REFUSALS
next_action: Re-fetch current directive identity, Analyst authority, MAIN/Relay collision state, main/candidate/PR/CI and retry exact-head conditional merge on the next MAIN run only if the same conditions still hold.
