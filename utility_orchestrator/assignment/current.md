# Current Utility Assignment

schema_version: 2
status: ASSIGNED
active_assignment_id: CTRL-20260921-0050-ELIGIBILITY-TIMEBASE-INVARIANCE
active_assignment_generation_id: UASSIGN-20260921T005250+0900-ELIGTIME-7D4A2C91
assigned_at: 2026-09-21T00:52:50+09:00
assigned_by: CONTROL_BRAIN
source_request_ids:
  - LIT-20260921-0030-ELIGIBILITY-TIMEBASE-INVARIANCE

objective: >-
  Determine whether stable v0.5 plasticity eligibility decay is intentionally
  episode/apply-count based or instead depends on non-semantic API partitioning.
  First establish the intended decay clock from stable source/docs/tests. If it
  is not explicit, execute one isolated DEV diagnostic that holds event-time
  spike/reward history and elapsed physical/model time fixed while varying only
  non-semantic process/apply partition count, then report eligibility immediately
  before the same later rewarded/reactivated event and the resulting target-edge
  weight delta.

temporary_role: V05_ELIGIBILITY_TIMEBASE_REPRODUCIBILITY_DIAGNOSTIC
temporary_mode: NON_EVIDENTIARY_DIAGNOSTIC_PROTOTYPE

target:
  authoritative_main: ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d
  source_area: src/sparkbrain/v05
  object: V05_PLASTICITY_ELIGIBILITY_TIMEBASE
  preferred_isolated_branch: research/utility-v05-eligibility-timebase-invariance-20260921

allowed_actions:
  - Re-fetch and read stable main source, docs, tests, and supported call sites needed to determine the intended eligibility decay clock.
  - If and only if the clock is not already contractually explicit, create one fresh utility-owned isolated diagnostic branch from the exact authoritative main above.
  - Before any outcome-bearing diagnostic, persist a prospective diagnostic contract fixing the two compared call partitions, identical event timestamps/reward sequence, identical elapsed physical/model time, observed eligibility point, target edge, weight-delta readout, and terminal mapping.
  - Execute at most one bounded DEV diagnostic under that fixed contract; record raw observations before terminal classification.
  - Run ordinary CI for the isolated diagnostic branch if needed to establish diagnostic validity.
  - Report exactly one terminal classification: PARTITION_INVARIANT, EXPLICIT_EPISODE_TIME_SEMANTICS, CALL_COUNT_DEPENDENT, or INVALID_DIAGNOSTIC.
  - Append one result under utility_orchestrator/results/2026-09-21/ and update Utility-owned state; do not edit this Control-owned assignment pointer.

forbidden_actions:
  - Do not alter, rerun, retune, rescore, relabel, reopen, or use as a rescue path CAND-V05-ELIGIBILITY-HISTORY-SPECIFICITY-01 or any consumed/formal identity.
  - Do not modify prospective contract e466bd89cfd4ab80dc970173a183638af815fe8b, outcome commit bd071d9023058d01f58d6f7ddacf35e820de51b6, result head 6ddcb7fec39dd017fbfe172885a994a98b503021, or its terminal ORDINARY_PER_EDGE_ELIGIBILITY_TRACE_REDUCTION.
  - Do not modify stable production semantics, main, immutable/frozen/formal/sealed/evidence/preserve/control refs, or merge any research PR.
  - Do not access held-out/evaluator-only data or official scorers, and do not create or consume FORMAL/PRE_FORMAL identities.
  - Do not create, promote, or classify a scientific candidate; do not set or change claim_ceiling, preformal_eligible, preformal_readiness, hold dimensions, or theory-backward accounting.
  - Do not interpret a timebase/API issue as mechanistic novelty or as evidence for H7/CAND-H7-RESP-01.
  - Do not use active MAIN/SUB/Relay scientific branches as fixtures or dependencies.
  - Do not change any scheduler, including Utility itself.
  - No outcome-responsive redesign, alternate partition after observing the result, rescue retry, parameter tuning, or second diagnostic run.

max_runs: 1
expiry: 2026-09-28T00:00:00+09:00
stop_condition: >-
  Stop immediately after source/docs/tests establish EXPLICIT_EPISODE_TIME_SEMANTICS;
  otherwise stop after the first fixed diagnostic reaches PARTITION_INVARIANT,
  CALL_COUNT_DEPENDENT, or INVALID_DIAGNOSTIC. If identical semantic history
  cannot be held fixed while varying only non-semantic partition count, classify
  INVALID_DIAGNOSTIC rather than redesigning the same assignment.
reporting_destination: utility_orchestrator/results/2026-09-21/CTRL-20260921-0050-ELIGIBILITY-TIMEBASE-INVARIANCE.md
evidentiary_status: NON_EVIDENTIARY_ARCHITECTURE_REPRODUCIBILITY_DIAGNOSTIC
scientific_authority: NONE
main_critical_path_dependency: false

hard_floor: >-
  No consumed-identity rerun/retune/rescore; no immutable/frozen/formal/evidence
  mutation; no evaluator leakage; no silent post-outcome repair; no bypass of
  prospective binding, STARTED/no-clobber, raw-before-score, preserve-before-read,
  exact binding, matched privilege/resources, or Evidence Analyst Formal authority.
