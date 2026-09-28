# Fast Forge — FLY-0 intent supersession guard prototype

generation_id: `FORGE-20260929T053548+0900-FLY0-INTENT-SUPERSESSION-GUARD-PROTOTYPE`
produced_at: `2026-09-29T05:35:48+09:00`
forge_id: `FORGE-FLY0-INTENT-SUPERSESSION-GUARD`
status: `FORGE_PROTOTYPE`
recommended_handoff: `NONE_UNTIL_CURRENT_HEAD_VERIFICATION`
evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
scientific_credit: `0`
new_scientific_result: `false`

Directive identity is unchanged at `8ce979b9ec0bc7eede5225c0403698f8886d3e8d` /
`1ba1e173344f36e14d0e21e6f3e823254e031f7d`. Durable Analyst is R169.
SB003 is allocated to PRIMARY MAIN but remains conditional/inactive behind M1-002.
This Forge probe is isolated and does not alter MAIN/Relay ownership.

Exact source head `3a21acf6412c4b8920b91e18dc07fef1fcfcfe12` adds a
`ModulationSupersessionGuard` plus focused tests. It addresses a bounded handoff
race where high-level state can change without changing the local sensorimotor
checkpoint. Frames carry a separate high-level authority epoch/token; a frame
minted under an older authority is rejected before the existing ModulationFrame
v2 bridge after authority is superseded. Rejection preserves local state and
bridge sequence. Fresh frames keep the unchanged v2 vocabulary
(`neutral`, `hold`, `permit_side`). Checkpoint/restore binds the guard
authority and nested bridge state transactionally.

The same wrapper/report covers structured, degree-rewired, random-sparse and
reactive variants. Current-head CI is not claimed: the available connector
showed no run/status entry for this source head, and an independent checkout
was unavailable in the automation container. Status therefore remains
`FORGE_PROTOTYPE`.

Ordinary reduction: an epoch/lease-style stale-command guard around the existing
hierarchical reactive/FSM-style modulation bus. The prototype adds no richer
goal vocabulary, direct motor command, continuous gain/bias or topology control.

Claim boundary: NON_EVIDENTIARY/NONCANONICAL; no biological fidelity/equivalence,
topology necessity/superiority, efficiency, composition contribution,
whole-system superiority, external validity, rich goal-conditioned behavior,
novelty, scientific support, scientific credit, or SYSTEM_BUILD completion is
established.

P0 `INC-GITHUB-MUTATION-RECURRENCE-20260928-001` remains OPEN. Branch creation
and both source-file writes succeeded. Two earlier attempts to publish this
history were refused before GitHub by the platform/runtime layer. No scheduler
state changed and no Work-backed path was used.
