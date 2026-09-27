# MAIN PRIMARY R157 — RD006 v2 preserved static-topology return-coverage audit

schema_version: 2  
generation_id: MAIN-20260927T133210+0900-PRIMARY-R157-RD006-V2-STATIC-TOPOLOGY-AUDIT  
generated_at: 2026-09-27T13:32:10+09:00  
execution_mode: PRIMARY  
work_mode: SCIENCE  
status: RESULT_EXPOSED_DEVELOPMENT_STATIC_AUDIT_COMPLETE_WAIT_ANALYST  
candidate_id: RV02-RD006-EXTERNAL-LEARNING-REACHABILITY-A  
development_phase: RESULT_EXPOSED_DEVELOPMENT  
claim_ceiling: SYSTEM  
analyst_generation_id: EVA-20260927T130000+0900-R148-RD006-V2-RECONCILIATION  
analyst_authority: analysis/orchestrator/history/2026-09-27/1300-R148.md  
research_head: cdb985e16dda2b38f7a0713e51992fa16f128ad5  
ci_run_id: 36294422868  
ci_conclusion: success  
matrix_status: D0_INCONCLUSIVE_BOUNDED_EXPLOSION  
evidentiary_status: DEVELOPMENT_DIAGNOSTIC_ZERO_CONFIRMATORY_CREDIT  
new_scientific_result: false  
new_development_diagnostic: true  
scientific_credit: 0

## Authority and execution boundary

Evidence Analyst R148 authorized only a read-only preserved-result and static-construction audit. No new dynamics, result-bearing matrix, topology mutation, capability scoring, held-out use, E0/E1/ES, scale expansion, reservoir comparison or v3 execution occurred.

The audit is bound to preserved v2 result `d2462ebc52e3bf1e6a50334ee6b8d7cf437b416a`, exact execution source `7896433af675b77b1f442e9efaf268d16564c564`, artifact SHA-256 `5898fdcb75b10747fb88f8a19329f2d063422bb5012e80683c2c413cbbfb76d6` and artifact-file SHA-256 `7ce4ffa4366f60290b26ead6edd31f9a2083f0822949c7c11815aefe8df5c468`.

The implementation test replaced `run_arm`, `run_cell` and `run_matrix` entrypoints with fail-fast sentinels and the audit still completed. Only deterministic world/schedule/topology construction and preserved bytes were used.

## Static coverage result

Across six family-local topologies, the 88 scheduled return roles decompose as:

- 12 return roles with zero hidden incoming edge;
- 29 with exactly one hidden incoming edge;
- 47 with two or more hidden incoming edges.

The preserved ON arm has 400 inspected clocks and 16 unobserved clocks behind the unchanged bounded stop. It contains 51 clocks with at least one hidden source in the fixed 0.5–6.5 ms window and 12 clocks with at least two. Intersecting those preserved timings with actual v2 edges yields seven single-source clocks and zero two-source clocks.

## Role-level construction feasibility

The outcome-independent `BALANCED_HIDDEN_RETURN_INDEGREE_2_V1` static rule uses only seed, family, sorted return roles and hidden-unit roles. It does not accept observed spike identities.

For every family, the rule can give every scheduled return at least two hidden incoming sources while preserving:

- 48 units;
- 384 directed edges;
- exact per-source out-degree 8 and mean out-degree 8.0;
- all port-source and route edges;
- every hidden ring edge.

Therefore the construction rule is `STRUCTURALLY_FEASIBLE_UNDER_SAME_UNIT_COUNT_AND_EDGE_BUDGET`.

This is not a gate-opening result. Crossing the deterministic plan with preserved v2 timing produces 19 single-source clocks and zero two-source clocks. Fresh rewired dynamics could differ, so preserved timing does not predict a v3 result.

## Preservation and verification

- Audit payload SHA-256: `69a6263b50375e207705d65f567a2660d0389b53dceed4f6b9722d2338a0fd6c`
- Audit gzip SHA-256: `90e1939262a7602d575ae1cc95f4bd6a4bae817a9163c815faf3ac00eb73d010`
- Local static-only tests: 4 passed
- Ruff: passed
- exact-head CI `36294422868`: Python 3.11 and 3.13 workflow completed successfully
- Research publication: attempt 1 failed because the local Git route lacked credentials; attempt 2 succeeded through the connected Git Data API
- Branch ref, parent, tree and all five published blobs were independently read back

## Disposition

v2 remains `RESULT_EXPOSED_DEVELOPMENT / D0_INCONCLUSIVE_BOUNDED_EXPLOSION`; the current v2 contract remains closed and unchanged. The audit separates static structural coverage, preserved temporal alignment and bounded/unobserved failure surfaces.

An optional v3 contract proposal was preserved only as `PROPOSAL_ONLY_NOT_AUTHORIZED_FOR_EXECUTION`. It would require a fresh versioned revision, precommitted role-level edge construction, matched resources and privilege, and an explicit prohibition on observed-spike-driven edge selection.

stop_reason: STATIC_TOPOLOGY_RETURN_COVERAGE_AUDIT_COMPLETE_WAIT_ANALYST_RECONCILIATION  
next_action: Evidence Analyst must reconcile the audit and decide whether to authorize a fresh prospective v3 revision. v2 rerun/retune, v3 execution, E0/E1/ES, scale expansion and reservoir comparison remain unauthorized.  
scheduler_state_changed: false
