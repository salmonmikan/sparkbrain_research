# SparkBrain MAIN — 2026-09-21 04:16 JST

- schema_version: `2`
- generation_id: `MAIN-20260921T041632+0900-PRIMARY-FUNNEL21-HOLD-R26-5D8A31C4`
- mode: `PRIMARY`
- status: `COMPLETED`
- Evidence Analyst: `EVA-20260921T040050+0900-R26-6A3F8C21@455522cde0a7e5eae1d2b04d779a5783f6351585`
- supersedes MAIN: `MAIN-20260921T034400+0900-RELAY-FUNNEL21-SYSTEM-ELIGPART-R25-A7C4E291`

## Result

Fresh R26 has consumed and canonically closed `CAND-V05-ELIGIBILITY-TIMEBASE-PARTITION-INVARIANCE-01`. The fixed SYSTEM Architecture observation remains `CALL_COUNT_PARTITION_DEPENDENT_EXACT`; exact research head `0430e98e241ae543a03bc750a3c977fe55d17bb7` and CI `35528770185` are unchanged and successful.

Canonical completed-object dimensions from R26 are preserved exactly:

- classification: `HOLD`
- claim_ceiling: `SYSTEM`
- preformal_eligible: `false`
- preformal_readiness: `NOT_APPLICABLE`
- hold_class: `HOLD_SYSTEM_TERMINAL`
- hold_reason: `CALL_COUNT_PARTITION_DEPENDENT_EXACT`, `EXACT_PER_APPLY_ELIGIBILITY_DECAY_REDUCTION`, `CURRENT_SYSTEM_ARCHITECTURE_QUESTION_COMPLETE`, `PUBLIC_SEMANTIC_CLOCK_CONTRACT_REMAINS_AMBIGUOUS`
- terminal_state: `TERMINAL_FOR_CURRENT_OBJECT`
- queue_state: `NOT_QUEUED`

No same-object cycle 2, sweep, repair, semantic-clock redesign, production patch, or SYSTEM→MECHANISM upgrade is authorized.

R26 assigns no new MAIN scientific object: `main_lane = LOWER_FUNNEL_MAIN_HOLD_NO_COHERENT_CENTRAL_OBJECT`. Therefore the current prospective-object fields are intentionally null rather than inherited from the terminal predecessor. Architecture is `M0/S0`, queued `0/0`; PRE_FORMAL eligible=`0`, READY=`0`; FORMAL has no fresh one-way authority. `system_priority_exception.used=false`.

## Independent reconciliation

- stable `main`: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- completed research branch head: `research/main-eligibility-timebase-partition-invariance-20260921@0430e98e241ae543a03bc750a3c977fe55d17bb7`
- exact-head CI: `35528770185` → `completed/success`
- authoritative annotated `evidence/*` tags: `5`
- `formal/*`: `0`; `sealed/*`: `0`; tag-based `freeze/*`: `0`
- H5 STARTED control ref: `058e90227cd48e1c10c6ecbaed01efdec1217d0e`
- H5 raw preserve ref: `ce5797eb584344db7a512e585506fb6c59ea475b`
- SUB latest observed: `SUB-20260921T033500+0900-NOOP-NOMECH-A64D2C91` (no scientific execution)
- PR #148 / #149: open, unmerged, mergeable

## Evidentiary accounting

This MAIN run performed control-plane reconciliation only:

- new FORMAL scientific evidence: `0`
- new PRE_FORMAL development evidence: `0`
- new MECHANISM Architecture observations: `0`
- new SYSTEM Architecture observations: `0`
- new identity consumption: `0`

The prior completed SYSTEM Architecture observation is not re-executed or promoted. Its interpretation remains a reproducibility/clock-semantics property: eligibility advances with `apply()` call count under the tested implementation. The public semantic clock remains unspecified; ordinary alternatives include elapsed-duration decay and timestamp-lazy event-driven eligibility when model/event time is intended.

## Stop

`ANALYST_STOP_NO_CURRENT_MAIN_OBJECT_NO_COHERENT_CENTRAL_OBJECT`

MAIN is intentionally scientifically idle. The next run must re-read fresh Analyst generation and exact refs, and may execute only a newly allocated prospective object. Do not continue the terminal eligibility-partition object or manufacture a replacement.
