# RV01 R01-17 freeze-readiness review — 2026-09-15

## Scope

This is a prospective technical/semantic review record for the distinct exposed-development protocol `rv01-r01-17-real-delay-causal-timing-v1`. No R01-17 candidate output was executed or inspected during this review.

Reviewed scientific source parent: `da5a67bf54bf60601f43e3be5c9f4f7481f51ee6`.
Current RV01 authoritative branch rechecked during review: `research/rv01-endogenous-transition@f72d840da0b3602971635698b4a15bf8f12585c4`.

## Findings

- R01-17 is distinct from consumed R01-16 and does not rescore, repair, rerun, or retune it.
- Seeds `141800` through `141804`, construction ranges, `0.5 ms` minimum learned-delay displacement, `0.5 ms` minimum downstream first-arrival shift, `0.05 ms` timing tolerance, F0/FD/SHAM arm semantics, and aggregate decision rule are fixed prospectively in the preregistration/source before any real acquisition.
- Initial physical delay is prospectively separated from training lag by `1.5–2.25 ms`; eligibility is tolerance-aware and does not use exact floating-point inequality.
- F0 and FD retain matched learned weights; only delay is reset in FD. SHAM is an exact F0 replay control.
- The raw evidence contract now retains every training exposure's deterministic pulses, learner observation results, before/after connection hashes, and post-exposure connection inventory, in addition to pre/post connection state and probe outputs.
- Pure synthetic scorer tests cover support, unsupported, mixed, construction-ineligible, and exact preregistered `0.5 ms` boundaries without invoking the real five-cell acquisition.
- Canonical protocol/status/decision records now identify R01-17 as prospective exposed-development work with no held-out/formal authority.
- The exactly-once workflow requires an exact source freeze and atomic STARTED/control ref, refuses retries and pre-existing preserve refs, preserves raw evidence before scoring, and treats failure after STARTED as terminal for this identity.
- One-shot remediation helpers used to close review findings are absent from the reviewed final tree.
- No R01-17 freeze, STARTED/control, raw preserve, or scored preserve ref existed at the final pre-freeze ref audit.

## Review disposition

No substantive scientific/integrity blocker remains in the reviewed protocol surface. Execution is GO only after CI is green on the exact final source SHA, that exact SHA is re-reviewed for concurrent movement, and freeze/STARTED/preserve absence is rechecked immediately before crossing the one-way boundary.

`USER_AUTHORIZED_REVIEW_GATE_OVERRIDE / HUMAN_REVIEW_WAIVED_BY_USER`

This marker waives only a literal independent-human-only gate. It does not waive exact-source, CI, prospective-contract, no-collision, raw-before-score, no-rerun, or immutable-evidence requirements.
