# Fast Forge — FLY-0 directional descending modulation green

generation_id: `FORGE-20260929T044715+0900-FLY0-DIRECTIONAL-MODULATION-GREEN`
produced_at: `2026-09-29T04:47:15+09:00`
forge_id: `FORGE-FLY0-DIRECTIONAL-MODULATION-CONTRACT`
status: `FORGE_INTERESTING`
recommended_handoff: `SYSTEM_BUILD_INPUT`
evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
scientific_credit: `0`
new_scientific_result: `false`

Human Directive identity is unchanged at `8ce979b9ec0bc7eede5225c0403698f8886d3e8d` /
`1ba1e173344f36e14d0e21e6f3e823254e031f7d`. Durable Analyst remains R168
(`266864682894af7745156ec899da3377cacc18fb`) and SB003 remains unallocated.
Control remains R117. M1-002 remains MAIN-owned at
`2a21d3e879f1db4e81a58273180ad2124e823a5e` over
`main@59fc994b39d0ba02682e972161bb46801592d25b`, no open PR, no Relay allocation,
so this isolated Forge probe has no ownership collision.

Exact source `4a68fde7cc3ba519a978810ab1002d1e9312f839` upgrades the prior bounded descending-modulation
bridge to `fly0-modulation-frame-v2`. In addition to `neutral` and `hold`,
it adds one coarse semantic mode: `permit_side(left|right)`. Matching side
permission allows the local controller's own ordinary step; a mismatch commits
a high-level veto without injecting an opposite motor action or mutating local
controller internals. A descending cut bypasses the high-level veto and restores
the ordinary local baseline.

The frame still binds monotonic sequence, TTL <= 4 local steps, exact local
checkpoint provenance and the versioned modulation contract. Invalid side use,
stale/expired/future-issued frames, provenance mismatch and schema mismatch fail
closed. Cross-layer restore remains transactional.

The same v2 interface is exercised against structured, semantic-surface-preserving
degree-rewired, semantic-surface-preserving random-sparse and ordinary reactive
variants. Acceptance covers neutral baseline, hold, matching directional permit,
mismatching directional veto, descending cut, independent local-feedback cut,
exact checkpoint/replay, invalid-frame fail-closed behavior and no partial bridge
advance on local failure.

CI run `36474193214` completed successfully on exact source `4a68fde7cc3ba519a978810ab1002d1e9312f839`.
Python 3.11 and 3.13 both passed lint, local readiness, tests and bundle
validation. The separate automation container could not clone GitHub because
external DNS was unavailable, so no separate container-local checkout run is
claimed.

Ordinary reduction remains hierarchical reactive/FSM or subsumption-style mode
selection with an explicit modulation bus. Continuous gain/bias and a richer
goal vocabulary remain deliberately omitted to avoid hidden tuning degrees of
freedom before durable SB003 allocation.

Engineering disposition: `FORGE_INTERESTING / SYSTEM_BUILD_INPUT`. This is
NON_EVIDENTIARY/NONCANONICAL and does not allocate SB003 or establish biological
fidelity/equivalence, topology necessity/superiority, efficiency, composition
contribution, whole-system superiority, external validity, rich goal-conditioned
behavior, novelty or scientific credit.

P0 `INC-GITHUB-MUTATION-RECURRENCE-20260928-001` remains OPEN. Isolated branch
creation succeeded on attempt 1. Source publication reached verified success on
attempt 2; the first source-publication error detail was not retained by the
orchestration result, so no specific failure class is asserted. No scheduler
state changed and no Work / Work-mode / Work-backed path was used.
