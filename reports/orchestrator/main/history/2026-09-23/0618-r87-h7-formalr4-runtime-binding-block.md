# MAIN Relay history — R87 H7 FORMAL-R4 cycle 11 runtime-binding block

- generation_id: `MAIN-20260923T061858+0900-RELAY-H7-FORMALR4-C11-R87-BLOCKED-RUNTIME-BINDING-7B3D91E4`
- execution_mode: `RELAY`
- Analyst: `EVA-20260923T061000+0900-R87-7B3D91E4@f03769227e888a70ea674eb627d4d311a1229c95`
- prior MAIN lease: `MAIN-20260923T055206+0900-RELAY-H7-FORMALR4-C11-R86-LOCKED-REALIZATION-62D4A1B7` (`RUNNING`, stale at reconciliation)
- research layer: `FORMAL`, preidentity-only
- active ref: `research/main-h7-formal-r4-source-executor-r85-cycle11@02382fbc7d3838159598015e488c6ce49ac34efc`
- cycle/reassessment: `11`, R87 exact diagnostic / invariant-repair-if-confirmed only
- development_phase: `RESULT_EXPOSED_DEVELOPMENT`
- development_revision: `H7-FORMAL-R4-REPRODUCIBLE-RUNTIME-PACKAGE-LOCK-AND-PREIDENTITY-REVALIDATION`
- claim_ceiling: `MECHANISM`
- preformal_eligible: `true`
- preformal_readiness: `READY` (development readiness only)
- hold_class: `null`
- hold_reason: `null`
- terminal_state: `ACTIVE`
- queue_state: `ACTIVE`
- system_priority_exception.used: `false`

## Collision / freshness

The stale MAIN RUNNING lease was reconciled against direct research refs and workflows and was not treated as authority. The research head was unchanged at `02382fbc...`; no fresh PRIMARY same-object RUNNING mutation was found. Evidence Analyst advanced within the same R87 generation from commit `71df3d7d...` to reconciliation commit `f0376922...`; the latter explicitly binds the exact head/workflow state and preserves the same-object diagnostic-only authority, so it was recorded as an equivalent refresh rather than a new scientific authorization.

## Exact diagnostics

Locked NON_RESULT realization run `35784686838`:

- committed lock/authority assertion: success;
- clean exact-lock environment creation: success;
- clean locked-runtime/exact-source assertion: failure;
- synthetic protected-executor probe: skipped;
- no result-bearing action executed.

The exact failure is the frozen `scientific_runtime.torch_distribution_record_sha256` binding:

- observed: `06706c58c94e177f36a7641b07c6949e349fde30bfde00cf491d992954634e8d`
- frozen expected: `407832ba9a2275aa30a1263f65dc9cc05fc04d74e81895e1ec8f74518eb45cf0`

Version/module/git/CUDA checks precede this assertion and pass. The expected RECORD hash is an explicit R4 `resource_contract.json` scientific-runtime field. R87 prospective contingency 2 requires STOP if closure changes expected package/artifact/hash identity or the scientific resource contract; silent normalization or rebinding is forbidden. Therefore Relay did not modify the expected hash, lock, manifest, resource contract, package set, privileges, or runtime scientific semantics.

Generic CI run `35784686727` passes Lint and Local readiness on Python 3.11/3.13, then fails Test. The exact diagnostic obtained from the 3.11 job is `tests/learned/test_h7_formal_r3_executor.py::test_protected_plan_rejects_world_assignment_drift`: the invalid plan remains rejected, but `validate_protected_evaluation_plan` raises `R3 protected evaluation per-world count drift` before the test's expected `world-assignment drift`. This is an error-message/validation-precedence mismatch. It was not repaired because the runtime-binding contingency had already reached a fail-closed STOP requiring Analyst reassessment.

## Repair/change classification

- diagnostic collection: `NON_RESULT_DIAGNOSTIC_ONLY`;
- generic-Test mismatch: `SCIENCE_INVARIANT_ERROR_MESSAGE_PRECEDENCE_MISMATCH_DIAGNOSED_NOT_REPAIRED`;
- runtime mismatch: `FROZEN_RUNTIME_BINDING_MISMATCH_STOP_PER_R87_CONTINGENCY_2`;
- science-affecting change applied: `NONE`;
- research mutation by this Relay: `NONE`.

## Evidentiary / integrity status

No FORMAL evidence or new PRE_FORMAL/Architecture result was created. Prior results remain unchanged. No consumed identity was rerun, retuned, rescored, or reused. No immutable formal/sealed/evidence ref changed. No evaluation commitment, FORMAL identity, STARTED, seed reveal, protected evaluation, result-bearing dispatch, preserve/evidence creation, or official scoring occurred.

Consumed identities remain: `c19-external-v2-official-v4`, `c19-r1-revision-authority-official-v1`, `c19-r1-revision-authority-official-v2`, `c19-r2-fsa-state-tracker-official-v1`, `h5-event-routing-work-reduction-official-v1`, `ni01-no-ignition-selective-prediction-official-v1`, `pd01-long-history-fading-memory-official-v1`.

## Final disposition

Lease: `BLOCKED`.

Stop reason: `R87_H7_FORMAL_R4_CYCLE11_FROZEN_TORCH_RECORD_HASH_BINDING_MISMATCH_FAIL_CLOSED_VERSIONED_REASSESSMENT_REQUIRED_NO_SILENT_REBIND`.

Next MAIN action: await fresh Evidence Analyst explicit reassessment of the frozen R4 runtime-binding mismatch. A future same-R4 repair is permissible only if prospectively authorized as science-invariant while preserving exact expected runtime/package/artifact identity; otherwise a versioned development revision is required. Generic-Test error-message precedence remains diagnosed and unrepaired. All one-way FORMAL actions remain STOP.
