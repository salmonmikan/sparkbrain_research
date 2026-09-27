# MAIN PRIMARY R156

schema_version: 2
generation_id: MAIN-20260927T112511+0900-PRIMARY-R156-RD006-PRESERVED-AUDIT
generated_at: 2026-09-27T11:25:11+09:00
execution_mode: PRIMARY
work_mode: SCIENCE
status: RESULT_EXPOSED_DEVELOPMENT_AUDIT_COMPLETE_WAIT_ANALYST
candidate_id: RV02-RD006-EXTERNAL-LEARNING-REACHABILITY-A
identity_namespace: rv02-rd006-external-learning-reachability-a-v1
development_phase: RESULT_EXPOSED_DEVELOPMENT
claim_ceiling: SYSTEM
analyst_generation_id: EVA-20260927T110000+0900-R146-P0-CLOSED-FORGE-PLURAL-BRIDGE-REVIEWED
analyst_authority: analysis/orchestrator/history/2026-09-27/1100-R146.md
allocation: RD006_D0_PRESERVED_CAUSAL_OPPORTUNITY_AUDIT
branch: research/rv02-rd006-external-learning-reachability-a
prior_result_head: 49b91ca801522f3d6685ebd22097a1e64f9234c9
audit_head: 2e4b27b620c7fdd2d4d1803df0f11f13b5ed28e8
audit_ci_run: 36288312007
audit_ci: SUCCESS
matrix_status: D0_INCONCLUSIVE_BOUNDED_EXPLOSION
evidentiary_status: DEVELOPMENT_DIAGNOSTIC_ZERO_CONFIRMATORY_CREDIT
new_scientific_result: false
new_development_diagnostic: true
scientific_credit: 0

## Authority and collision checks

MAIN re-read policy from `main@cf0bc45262824f1fe282ccd7b785b3ea50be2099`, the active Human Directive index, HUMAN-20260927-001, HUMAN-20260927-002 and the persistence/P0 directives applicable to the current object. Evidence Analyst R146 retains the R145 allocation for a preserved-result causal-opportunity audit only. MAIN R155 lease was complete and no newer Relay-owned MAIN mutation was present.

No FORMAL action, v1 rerun/retune, E0/E1/ES, scale expansion, reservoir comparison, lag/threshold/gain/stimulus/topology change or event-ceiling expansion was authorized.

## Preserved inputs and output identity

- preserved result head: `49b91ca801522f3d6685ebd22097a1e64f9234c9`
- preserved source head: `b4fbd9cc92f9e9d02f4ec1ff69084ab31f924b0c`
- preserved artifact SHA-256: `c27951973b25a83ea3a23ce16b97e6634ac513929aee605c8af417410e12209c`
- audit payload SHA-256: `269138e81d7c282cc809b2920f0b381e9afa6ab5a3e49a45c5f707a928763341`
- compressed audit file SHA-256: `0e500f9788aeddaa42e8db666568d1cc2122040a20fe350b6f855e6bb35b3dac`
- exact published audit head: `2e4b27b620c7fdd2d4d1803df0f11f13b5ed28e8`
- exact-head CI run: `36288312007`, success on Python 3.11 and 3.13

The audit reconstructs only deterministic v1 topology and schedule, verifies their per-cell digests, and combines them with preserved clock/spike/update rows. It does not use the outputs of any later local dynamics invocation.

## Audit findings

The preserved artifact contains 816 inspected clocks plus one bounded-explosion decision point. The complete failure census is:

- `NO_STRUCTURAL_RETURN_EDGE`: 124
- `STRUCTURAL_EDGE_NO_HIDDEN_SPIKE`: 684
- `HIDDEN_SPIKE_OUTSIDE_LAG`: 8
- `ELIGIBLE_SINGLE_SOURCE_ONLY`: 0
- `ELIGIBLE_MULTI_SOURCE`: 0
- `BOUNDED_EXPLOSION_BEFORE_DECISION`: 1

Every family has structural hidden-to-scheduled-visible return edges at some inspected clocks, so v1 is not globally missing return edges. The only eight clocks with a spike from a structurally connected hidden source are in the ON arms of shared-prefix and capacity-pressure. All eight have lag `0.0 ms`, which is `0.5 ms` below the fixed `0.5–6.5 ms` window.

The ordinary external learner traces only externally scheduled PORT targets. All 356 preserved ordinary updates are `PORT_TO_PORT`; direct `PORT_TO_HIDDEN`, `HIDDEN_TO_PORT` and `HIDDEN_TO_HIDDEN` updates are impossible under the actual schedule/trace rule. Hidden firing in ON arms is therefore an indirect PORT-dynamics effect, not direct hidden-return credit assignment.

For opposing-reversal ON, all 32 preserved pre-ceiling clocks have structural return edges but no spike from a connected hidden source. The failed clock targets PORT 9 and has five structural hidden incoming sources, but no decision row exists. The remaining 16 clocks were not inferred.

## Verification-procedure nonconformance

During initial local verification, the pre-existing `tests/test_rv02_rd006_external_learning_reachability.py` was invoked alongside the audit tests. That module calls `run_cell`/`run_arm`, causing non-persisted local dynamics despite the R145 restriction. Its outputs were not used, scored or persisted, and no preserved v1 bytes were changed. Once detected, no further dynamic test was run. The audit artifact and derivation remain preserved-byte-only.

Classification: `NON_PERSISTED_LOCAL_DYNAMIC_UNIT_TEST_INVOCATION`. This is a procedure nonconformance requiring Analyst visibility, not a new scientific result and not a basis for changing v1.

## Publication reliability

Research-branch publication used three total attempts for the same purpose:

1. local git push failed before GitHub because HTTPS credentials were unavailable;
2. GitHub Git Data preparation failed when the compressed-artifact blob request disconnected before a branch mutation;
3. after ref/idempotence recheck, Git Data blob/tree/commit/ref publication succeeded non-force.

Independent readback confirmed branch head, commit parent/tree, all text blob SHAs and the remote compressed artifact SHA-256. The successful route did not overwrite a newer generation.

## Lifecycle and next action

The v1 result remains `D0_INCONCLUSIVE_BOUNDED_EXPLOSION` and phase remains `RESULT_EXPOSED_DEVELOPMENT`. The audit narrows the failure surface to structural-target coverage, connected-source silence, zero-lag timing, an external learner that cannot directly update the PORT/hidden boundary, and one bounded-instability arm. It does not establish capability, comparative support, composition contribution or novelty.

stop_reason: PRESERVED_RESULT_CAUSAL_OPPORTUNITY_AUDIT_COMPLETE_WAIT_ANALYST_RECONCILIATION
next_action: Evidence Analyst must reconcile the audit and procedure nonconformance before authorizing any explicit versioned revision. v1 rerun/retune, E0/E1/ES, scale expansion and reservoir comparison remain closed.
scheduler_state_changed: false
