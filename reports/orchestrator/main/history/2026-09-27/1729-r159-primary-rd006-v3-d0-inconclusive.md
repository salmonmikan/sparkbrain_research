# MAIN PRIMARY R159 — RD006 v3 bounded D0 matrix

schema_version: 2
generation_id: MAIN-20260927T172900+0900-PRIMARY-R159-RD006-V3-D0
generated_at: 2026-09-27T17:29:00+09:00
execution_mode: PRIMARY
work_mode: SCIENCE
status: RESULT_EXPOSED_DEVELOPMENT_D0_INCONCLUSIVE_WAIT_ANALYST
candidate_id: RV02-RD006-EXTERNAL-LEARNING-REACHABILITY-A
development_phase: RESULT_EXPOSED_DEVELOPMENT
revision: v3-d0-execution
claim_ceiling: SYSTEM
analyst_generation_id: EVA-20260927T170004+0900-R151-RD006-V3-D0-DYNAMIC-GATE-CLARIFIED
analyst_authority: analysis/orchestrator/history/2026-09-27/1700-R151.md
research_branch: research/rv02-rd006-external-learning-reachability-a-v3-d0-execution
execution_source_head: 8867c0565e25a0c76749c12eec7f4c03238b7aef
result_head: 540fa54f45a8cdc467eb2695270035cb9332f2fb
ci_run_id: 36306014977
ci_conclusion: success
matrix_status: D0_INCONCLUSIVE_BOUNDED_EXPLOSION
evidentiary_status: DEVELOPMENT_ZERO_CONFIRMATORY_CREDIT
new_scientific_result: false
new_development_diagnostic: true
scientific_credit: 0

## Authority and exact execution surface

Evidence Analyst R150 authorized exactly one bounded v3 D0 matrix from static-preflight head `6b273e531c22729759cacabcced9df3319227a8e`; R151 prospectively clarified that the dynamic gate requires actual hidden spikes, distinct source IDs, an eligible non-negative source-to-current-return edge and an observed 0.5–6.5 ms lag.

The result-bearing executor was implemented on a distinct branch and preserved the static module's fail-closed dynamic sentinels. It retained the fixed six families, OFF/ON ordinary external-learning factor, hidden-return learning OFF, seed 92701, scale 1, 48 units, degree 8, threshold 0.5, weight 0.05, delay 5.0 ms, boundary gain 4.0, input magnitude 1.0, 5.5 ms schedule and fixed event/spike ceilings.

Static path counts and dynamically eligible actual-spike counts are stored separately. OFF and ON are separate execution cells. Capability scoring and held-out access remain absent.

## Verification before result exposure

- non-result-bearing v3 static and D0 contract tests: 15 passed;
- local readiness: PASS;
- targeted Ruff: PASS;
- full local collection unavailable only because optional `fastapi`, `jsonschema` and `torch` packages are absent from the scheduler runtime;
- exact-head CI `36306014977`: Python 3.11 and 3.13 both succeeded, including lint, readiness, full tests and bundle validation;
- executor source branch publication: attempt 1 succeeded and branch head, parent, tree and all four blobs were independently read back.

The first local runner invocation stopped during module import with `ModuleNotFoundError: sparkbrain` because the clean worktree did not have an installed package path. No manifest, Field or matrix was created. The source and contract were unchanged; the same exact source head was then invoked with the science-invariant environment correction `PYTHONPATH=src`. That was the sole matrix execution.

## Matrix result

The closed matrix result is `D0_INCONCLUSIVE_BOUNDED_EXPLOSION`.

- execution cells: 12;
- complete non-exploded cells: 11;
- bounded cells: 1;
- gate-open cells: 0;
- planned clocks: 832;
- inspected clocks: 816;
- hidden spikes: 144;
- ordinary external-learning updates: 356, all `PORT_TO_PORT`.

The `opposing-reversal / external_learning_on` cell reached the unchanged `max_events_per_run` guard at its 33rd scheduled clock, after preserving 32 of 48 clocks. The ceiling was not raised.

Only `shared-prefix / ON` and `opposing-reversal / ON` contained dynamically eligible hidden-source clocks. There were seven such clocks; every one had exactly one distinct eligible source. The observed maximum was 1, below the fixed requirement of 2 at the same return clock in a complete non-exploded execution cell.

Other ON cells produced hidden firing without a dynamically eligible source at the current scheduled return. Every OFF cell completed with zero hidden firing. These differences remain diagnostic only.

## Preservation and integrity

The complete gzip artifact, closed manifest and result summary were published atomically at result head `540fa54f45a8cdc467eb2695270035cb9332f2fb` on attempt 1 and independently read back.

- artifact logical SHA-256: `a71e324014b92ecf5680608f60f78e431c192f353d29af0633193546eec7a8da`;
- artifact file SHA-256: `ad7dc60af79681a30d67f1c0d2a4e39607a8984122f52bf9a65949950772b3f9`;
- uncompressed SHA-256: `567293813f6391fc6fae528fb4043deb3da75eeaad6a6ad2aeb73c008b8fc4f5`;
- internal logical digest recomputation matched.

RD006 v1/v2 remain preserved and closed as `D0_INCONCLUSIVE_BOUNDED_EXPLOSION`. RD005 remains `CONSUMED_ONE_WAY` and unchanged. No second matrix, retune, ceiling change, E0/E1/ES, scale/reservoir work, learner-boundary change or capability scoring occurred.

## Disposition

The static topology is constructible and ordinary external learning can coincide with hidden firing, but the required two-source dynamic reachability was not established. Because one ON cell remained bounded, this is an inconclusive development result rather than a universal negative.

The result does not establish ordinary-learning contribution, hidden-return learning, capability, composition contribution, scientific novelty or confirmatory evidence. Scientific credit remains zero.

stop_reason: V3_D0_INCONCLUSIVE_BOUNDED_EXPLOSION_WAIT_FRESH_ANALYST_RECONCILIATION
next_action: Evidence Analyst must reconcile the preserved v3 D0 result. The executed revision must not be rerun or redesigned without fresh authority; all later stages remain unauthorized.
scheduler_state_changed: false
