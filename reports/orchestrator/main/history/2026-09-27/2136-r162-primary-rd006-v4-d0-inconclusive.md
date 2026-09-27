# MAIN PRIMARY R162 — RD006 v4 one-shot D0 preserved

generated_at: 2026-09-27T21:36:47+09:00
generation_id: MAIN-20260927T213647+0900-PRIMARY-R162-RD006-V4-D0-INCONCLUSIVE
execution_mode: PRIMARY
work_mode: SCIENCE
status: RESULT_EXPOSED_DEVELOPMENT_V4_D0_PRESERVED_WAIT_ANALYST
candidate_id: RV02-RD006-EXTERNAL-LEARNING-REACHABILITY-A
revision: v4-port-to-hidden-trace-boundary-d0-execution
claim_ceiling: SYSTEM
analyst_allocation: EVA-20260927T200051+0900-R154-RD006-V4-D0-MATRIX-AUTHORIZATION
analyst_clarification: EVA-20260927T210004+0900-R156-RD006-V4-ATTRIBUTION-CLARIFICATION
new_scientific_result: false
scientific_credit: 0

## Authority and collision check

Current main policy, the applicable Human Directives, Analyst R154/R156, MAIN
R161, Control R96, the MAIN lease and Relay collision state were re-fetched.
Analyst target head remained
`0359aea01323bcf6d11e311242ed51ba6c087dd5`; MAIN reports remained R161 at
`08ae5aeb797f705a38fcd4e62598b16b179ea51e`; the preflight ref remained
`78594102ea03fe3ffc0f6e1e0b8b94dd66351005`. No competing Relay execution or
new v4 result was observed.

## Execution-source freeze

A distinct result-bearing package was created from the exact preflight head
without changing the preflight module or learner:

- branch:
  `research/rv02-rd006-external-learning-reachability-a-v4-d0-execution`
- source commit: `44bef35c90f24a11e27000e3c328778733da92b6`
- source tree: `040215d8f260f0b9084558cde4d65ce0755b92e5`
- exact-source CI: run `36319160839`, success on Python 3.11 and 3.13

Repository-wide ruff, readiness, full pytest and bundle validation passed
locally after installing the same declared CI extras. The adapter fixes the
12-cell order, config guards, measurement schema, no-clobber output,
append-only progress preservation, exact-head checks, and closed
capability/held-out entrypoints.

The source publication used two attempts. Attempt 1 failed at local Git
authentication before GitHub mutation. After fresh ref readback, attempt 2
used the Git object API; every blob and the exact local tree matched, and the
branch was independently read back.

## One-shot result

The authorized matrix was invoked exactly once from the frozen source commit.
No rerun, retune or rescore occurred.

- result commit: `50112626ef6a4da364e3fa9268e8feb0d723ea7f`
- result tree: `ef12cc8279b3043ef6dfc2577f155ed4e3bdbb15`
- result CI: run `36319533095`, success on Python 3.11 and 3.13
- raw artifact:
  `artifacts/rv02_rd006/external_learning_reachability_a_v4_d0_execution/attempt-001/artifact.json.gz`
- raw file SHA-256:
  `62b3ffb6d52926b583b006799d88511c9f840b626bc776cdcaf6ee2f857faf61`
- internal artifact digest:
  `e40a88cd596b79d1a6b78030c8f7ea3baac5fc5c8579551b7494b37f6b89d3ba`
- deterministic compressed progress journal SHA-256:
  `47085c3eb1f877f069d1e12659dc336ad94e7612c6db4d29f3879664eaba5003`

The result publication succeeded on its first attempt and was independently
read back, including the exact result parent, tree and artifact/summary blobs.

## Fixed readout

- matrix status: `D0_INCONCLUSIVE_BOUNDED_EXPLOSION`
- 12 cells started; 11 normally completed; 1 was bounded
- gate-open ON cells: 0
- hidden spikes: OFF 0; ON 148
- maximum dynamically eligible hidden sources at one return clock:
  OFF 0; ON 1
- ON learner updates: 356 PORT-to-PORT; 58 PORT-to-hidden
- prohibited updates: 0
- new edges: 0

The bounded cell was `opposing-reversal / external_learning_on`; it hit the
fixed `max_spikes_per_run` bound at event `rd006-v2-ext-000032` and is
preserved as a non-retryable result exposure.

Ordinary learning ON produced hidden activity where OFF produced none, but
the same-clock two-source return gate remained closed. Because ON contains both
retained PORT-to-PORT learning and the added PORT-to-hidden boundary, the
contrast estimates the complete ordinary-learning package effect and cannot
identify the incremental PORT-to-hidden contribution.

## Integrity and stop

RD005 remains consumed and untouched. RD006 v1/v2/v3 remain closed. No
capability/held-out work, E0/E1/ES, second matrix, scale or reservoir comparison
was executed. This development result has zero confirmatory credit and does not
establish composition contribution, novelty or capability improvement.

stop_reason:
`V4_D0_ONE_SHOT_PRESERVED_GATE_CLOSED_WAIT_FRESH_ANALYST_RECONCILIATION`

next_action: Evidence Analyst reconciles exact result commit
`50112626ef6a4da364e3fa9268e8feb0d723ea7f`. Any further science-affecting
work requires a fresh prospective revision and authority.

scheduler_state_changed: false
