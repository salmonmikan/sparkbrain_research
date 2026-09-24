# MAIN RELAY — H7 exact-blob binding repaired; waiting for fresh Analyst exact binding

- schema_version: `2`
- generation: `MAIN-20260924T105345+0900-RELAY-H7-R111-EXACT-BLOB-REPAIR-AWAITING-ANALYST`
- execution_mode: `RELAY`
- status: `WAITING_EXTERNAL`
- canonical object: `CAND-H7-RESPONSIBILITY`
- research layer: `PRE_FORMAL`
- development phase/revision: `RESULT_EXPOSED_DEVELOPMENT / R5_UNCHANGED`
- authorized scientific cycle: `12`; no extension
- claim ceiling: `MECHANISM`

## Authority / collision

Latest Evidence Analyst remains R111 at `2f1409da8d47525cbb1058ce9c7eebf8ef80ef2c`. The prior MAIN lease was `WAITING_EXTERNAL`, not PRIMARY `RUNNING`, so no same-object collision existed. Frozen H7 science remains unchanged at `2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`.

Funnel state is preserved exactly: `preformal_eligible=true`, `preformal_readiness=READY`, `hold_class=null`, `hold_reason=null`, `terminal_state=ACTIVE`, `queue_state=QUEUED`, `system_priority_exception=false`, `RESULT_EXPOSED_DEVELOPMENT / R5_UNCHANGED`.

## Science-invariant repair

The independently refreshed controller bundle exposed one pre-identity implementation binding defect: `artifacts/formal_h7_r5/launch_path_contract.json` still named the prior formal-launch workflow blob even though the workflow itself had already changed. This mismatch would fail closed before identity creation.

Relay changed only that stale blob binding. The repaired controller head is `af3aa97574c365e3e918c3d4d012faa4886760d0`. Its exact controller script, formal-launch workflow and plumbing-readiness workflow blobs now equal the three values recorded in the launch contract. No science-affecting field or scientific source changed.

R111 exact-bound the pre-repair controller, so Relay did not reuse R111 to cross FORMAL. The repaired controller remains dormant pending a fresh Evidence Analyst exact-binding generation.

## Evidentiary / integrity status

- new scientific result: `false`
- evidentiary status: `NON_RESULT_SCIENCE_INVARIANT_EXACT_BINDING_REPAIR`
- prior results preserved unchanged: `true`
- consumed FORMAL identities: `7`, unchanged
- active H7 identity / STARTED: `null / false`
- protected evaluation / held-out access: `false`
- result-bearing workflow dispatched: `false`
- raw production / preservation: `false / false`
- official scoring / PASS-FAIL: `false / false`
- immutable/formal/sealed/evidence ref mutation: `false`
- science-affecting change: `false`
- FORMAL hard floor: respected

## Stop / next MAIN action

Stop reason: `REPAIRED_CONTROLLER_HEAD_REQUIRES_FRESH_EVIDENCE_ANALYST_EXACT_REBIND_BEFORE_ANY_FORMAL_START`.

Wait for Evidence Analyst to inspect and exact-bind the repaired controller head with the unchanged frozen H7 science. Only a fresh subsequent GO_ONCE may permit one bridge arm / FORMAL dispatch. Until then remain prestart.
