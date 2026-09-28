# Fast Forge latest — FLY-0 directional descending modulation green

Status: FORGE_INTERESTING / SYSTEM_BUILD_INPUT / NON_EVIDENTIARY / NONCANONICAL.

Exact source `4a68fde7cc3ba519a978810ab1002d1e9312f839` implements `fly0-modulation-frame-v2` with
`neutral`, `hold`, and a coarse `permit_side(left|right)` permission gate.
Across structured, degree-rewired, random-sparse and reactive variants, matching
permission allows the local controller's ordinary step, mismatching permission
vetoes it without direct motor substitution, and a descending cut restores the
local baseline. Existing checkpoint/provenance, fail-closed, transactional
restore and local-feedback-cut guarantees remain intact.

CI `36474193214` is green on Python 3.11 and 3.13, including lint, local
readiness, tests and bundle validation.

Durable Analyst remains R168; SB003 remains unallocated. No scientific claim or
credit is created.

Authoritative history: `reports/fast_forge/history/2026-09-29/0447-fly0-directional-modulation-green.md`
