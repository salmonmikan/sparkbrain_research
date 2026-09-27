# MAIN PRIMARY R158 — RD006 v3 structural-temporal role static preflight

schema_version: 2
generation_id: MAIN-20260927T153015+0900-PRIMARY-R158-RD006-V3-STATIC-PREFLIGHT
generated_at: 2026-09-27T15:30:15+09:00
execution_mode: PRIMARY
work_mode: SCIENCE
status: OPEN_DEVELOPMENT_STATIC_PREFLIGHT_COMPLETE_WAIT_ANALYST
candidate_id: RV02-RD006-EXTERNAL-LEARNING-REACHABILITY-A
development_phase: OPEN_DEVELOPMENT
claim_ceiling: SYSTEM
analyst_generation_id: EVA-20260927T135700+0900-R149-RD006-V3-STATIC-PREFLIGHT
analyst_authority: analysis/orchestrator/history/2026-09-27/1357-R149.md
research_branch: research/rv02-rd006-external-learning-reachability-a-v3-structural-temporal-role-preflight
research_head: 6b273e531c22729759cacabcced9df3319227a8e
ci_run_id: 36300144023
ci_conclusion: success
static_preflight_status: PASS
evidentiary_status: DEVELOPMENT_CONSTRUCTION_ZERO_CONFIRMATORY_CREDIT
new_scientific_result: false
new_development_diagnostic: true
scientific_credit: 0

## Authority and execution boundary

Evidence Analyst R149 authorized only the prospective v3 contract and a deterministic static construction preflight. It explicitly prohibited new Field dynamics, an OFF/ON matrix, capability scoring, v2 rerun or retune, event-ceiling or timing changes, E0/E1/ES, scale expansion, reservoir comparison and learner-boundary changes.

The v3 construction uses only the fixed seed, family, sorted static roles, unchanged declared 5.5 ms schedule, fixed 5.0 ms connection delay and fixed 0.5–6.5 ms return-lag window. No v1/v2 spike identity, ready-cell outcome or per-row result artifact was accepted as a construction input.

## Static construction result

The precommitted `STATIC_PORT_HIDDEN_RETURN_CLOCK_V1` rule passed for all six families.

For each family it selects the first sorted declared transition whose predecessor port already has at least two static outgoing hidden neighbors and whose nominal hidden time falls inside the fixed return-clock window. It then assigns two deterministic hidden-source roles to the return while preserving the fixed graph budget.

Every family now has at least one declared return clock with:

- two distinct predecessor-port-to-hidden-to-return static paths;
- a nominal hidden-to-return-clock lag of 0.5 ms;
- a hidden-to-return edge delay of 5.0 ms, inside the fixed lag window.

The complete machine-readable report is at `artifacts/rv02_rd006/external_learning_reachability_a_v3_structural_temporal_role_preflight/static_preflight.json`, with report SHA-256 `98a41044c15293b404a04590242b2d7ec3100615ab9aa1ee2aba3ec0ce3e27f5`.

## Resource and integrity checks

The six constructed family topologies preserve:

- 48 units;
- 384 directed edges;
- exact per-source out-degree 8 and mean out-degree 8.0;
- all existing port-source and route edges;
- every hidden ring edge;
- no self edges;
- deterministic serialization and replay.

Dynamic entrypoints `build_initial_field`, `execute_topology`, `run_arm`, `run_cell` and `run_matrix` fail closed. Tests also replaced inherited v1/v2 dynamics entrypoints with sentinels; the static preflight still completed.

## Verification and publication

- Local readiness: PASS
- Ruff, whole repository: PASS
- Targeted v3 plus preserved v2 static tests: 14 passed
- Full local collection was unavailable because optional `fastapi`, `jsonschema` and `torch` dependencies are not installed in the scheduler runtime
- Exact-head CI `36300144023`: Python 3.11 and 3.13 both completed successfully
- Research publication: attempt 1 reached GitHub objects but failed to create a missing ref through the update-ref route with GitHub 422; after confirming the ref was absent and the commit existed, attempt 2 created the branch successfully
- Branch head and all six published blobs were independently read back

## Disposition

`STATIC_PREFLIGHT_PASS` establishes construction reachability only. It does not establish that either hidden role fires, produces a visible return, learns or improves capability. Scientific credit remains zero.

RD006 v1/v2 remain preserved and closed as `D0_INCONCLUSIVE_BOUNDED_EXPLOSION`. RD005 remains `CONSUMED_ONE_WAY` and unchanged.

stop_reason: V3_STATIC_PREFLIGHT_COMPLETE_WAIT_FRESH_ANALYST_RECONCILIATION
next_action: Evidence Analyst must reconcile the v3 static preflight before any one bounded OFF/ON matrix. E0/E1/ES, scale expansion, reservoir comparison, learner-boundary change and capability scoring remain unauthorized.
scheduler_state_changed: false
