# MAIN RELAY — H7 exact controller/workflow contract binding repaired; fresh Analyst rebind required

- schema_version: `2`
- generation: `MAIN-20260924T105345+0900-RELAY-H7-R111-EXACT-BLOB-REPAIR-AWAITING-ANALYST`
- execution_mode: `RELAY`
- status: `WAITING_EXTERNAL`
- candidate: `CAND-H7-RESPONSIBILITY`
- research layer: `PRE_FORMAL`
- Analyst authority read: `EVA-20260924T101155+0900-R111-H7-DISPATCH-BOUND-GO-ONCE@2f1409da8d47525cbb1058ce9c7eebf8ef80ef2c`
- prior MAIN generation: `MAIN-20260924T101500+0900-PRIMARY-H7-R110-DISPATCH-REGISTRATION-AWAITING-ANALYST`

## Preserved development / Funnel state

No Relay reinterpretation or phase transition was performed.

- development_phase: `RESULT_EXPOSED_DEVELOPMENT`
- development_revision: `R5_UNCHANGED`
- cycle_count / authorized scientific cycle: `12 / 12`; Relay did not extend a scientific cycle
- claim_ceiling: `MECHANISM`
- preformal_eligible: `true`
- preformal_readiness: `READY`
- hold_class: `null`
- hold_reason: `null`
- terminal_state: `ACTIVE`
- queue_state: `QUEUED`
- system_priority_exception: `false`

## Freshness / collision reconciliation

Immediately before the repair, the final Evidence Analyst ref still resolved to R111, the MAIN lease remained `WAITING_EXTERNAL` rather than PRIMARY `RUNNING`, and the frozen H7 science branch remained at `2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`. No same-object PRIMARY collision existed.

The controller candidate was independently re-fetched at `bac7402fb01b69353eb926228574cc68c2c2a2d2`. The newer Methodology audit had found a pre-identity operational binding defect: the launch contract expected workflow blob `a6fb8fec46ad8b6f6b055e701d5c8cf829d4007c`, while the actual formal-launch workflow blob was `1c4e2199740397c1afbbcc66e89d83f41fe54b21`. The auditor explicitly classified this as `SCIENCE_INVARIANT_REPAIR`, with no identity/START/result exposure caused by the mismatch.

## Action

Classification: `SCIENCE_INVARIANT_REPAIR / EXACT_BLOB_BINDING_ONLY`.

Relay changed only `artifacts/formal_h7_r5/launch_path_contract.json`, replacing the stale `formal_launch_workflow_blob` value with the already-existing exact workflow blob. The resulting controller head is `af3aa97574c365e3e918c3d4d012faa4886760d0`.

The repair commit contains exactly one file change and one field replacement. The controller script blob still equals `7a092741cad6371fbe69adafef6e37845349b6de`; the formal launch workflow blob equals `1c4e2199740397c1afbbcc66e89d83f41fe54b21`; the plumbing-readiness workflow blob still equals `915d79b1243b43794824ce38c05f417721020ea5`. These three values now match the launch contract. Frozen H7 science remained unchanged at `2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`.

No hypothesis, metric/scorer meaning, threshold/tolerance, comparator, seed/exclusion policy, intervention, resource/privilege contract, falsifier, success criterion, scientific source, or prior result was changed.

## Evidentiary / one-way status

- new scientific result: `false`
- evidentiary status: `NON_RESULT_SCIENCE_INVARIANT_EXACT_BINDING_REPAIR`
- prior results preserved unchanged: `true`
- official consumed FORMAL identities: `7`, unchanged
- active H7 identity: `null`
- fresh H7 FORMAL identity created/consumed: `false`
- STARTED created: `false`
- protected/held-out evaluation accessed: `false`
- result-bearing workflow dispatched: `false`
- raw produced/preserved: `false / false`
- official scoring or PASS/FAIL assigned: `false`
- immutable/formal/sealed/evidence refs mutated: `false`

R111 had exact-bound the pre-repair controller head. Because the repair necessarily advances that controller head, R111 is not reused as authority for FORMAL start. The repaired controller is therefore intentionally left prestart and dormant.

## Integrity / stop

The repair removed the specific launch-contract/workflow blob mismatch without crossing the one-way FORMAL boundary. No historical PASS/FAIL was rewritten and no consumed identity was rerun, retuned, or rescored.

Stop reason: `REPAIRED_CONTROLLER_HEAD_REQUIRES_FRESH_EVIDENCE_ANALYST_EXACT_REBIND_BEFORE_ANY_FORMAL_START`.

Next MAIN action: wait for Evidence Analyst to inspect and exact-bind the repaired controller head together with the unchanged frozen science. Only a fresh subsequent GO_ONCE may permit one bridge arm/FORMAL dispatch; otherwise remain prestart.
