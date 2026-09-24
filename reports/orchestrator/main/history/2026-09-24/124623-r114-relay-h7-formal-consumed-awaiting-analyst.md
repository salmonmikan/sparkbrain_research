# MAIN RELAY — H7 R114 FORMAL completed and consumed; fresh Analyst required

- schema_version: `2`
- generation: `MAIN-20260924T124623+0900-RELAY-H7-R114-FORMAL-CONSUMED-AWAITING-ANALYST`
- execution_mode: `RELAY`
- status: `WAITING_EXTERNAL`
- canonical object: `CAND-H7-RESPONSIBILITY`
- current Analyst layer/funnel state preserved exactly: `PRE_FORMAL / MECHANISM / READY / QUEUED / ACTIVE / RESULT_EXPOSED_DEVELOPMENT / R5_UNCHANGED`
- authorized scientific cycle: `12`; Relay did not extend or reassess the cycle
- repair/change classification: `NO_SCIENCE_CHANGE_BY_RELAY; EXTERNAL_FORMAL_OUTCOME_RECONCILIATION_AND_MAIN_MAILBOX_PERSISTENCE`

## Freshness / collision / authority

Relay re-fetched Evidence Analyst R114 and verified that `ops/evidence-analyst-handoff` is still exactly `1824290d67fdf06494c3849fa687997ec29137cf`; no superseding Analyst generation exists at this observation. R114's one-shot authority had already been used by PRIMARY and is not reusable after identity creation/START.

The current MAIN lease was `WAITING_EXTERNAL`, not a fresh PRIMARY `RUNNING` lease, so no same-object PRIMARY collision existed. Fast Forge latest is `FORGE-20260924T123200+0900-NOOP-R114-H7-FORMAL-ACTIVE-GATED`; it observed the top-level H7 workflow only, did not inspect result surfaces, and did not mutate H7. Control R55 was read as strategy only and is older than the R114 execution state.

Frozen science remains `research/main-h7-formal-r5-runtime-identity-r88-cycle12@2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`. Exact controller remains `research/main-h7-r5-launch-plumbing-r111-workflow-dispatch@af3aa97574c365e3e918c3d4d012faa4886760d0`. Relay made no change to either.

## External FORMAL completion observed

Previously dispatched result-bearing workflow `35951118916` is now `completed / success`, attempt `1`, on exact controller `af3aa97574c365e3e918c3d4d012faa4886760d0`.

All three one-way jobs completed successfully in the required order:

1. fresh identity materialized and STARTED create-only;
2. target-blind raw produced only after STARTED and remotely preserved before target access;
3. scoring performed only after remote-preserve verification, then formal/sealed/evidence refs created without clobber.

No rerun, retune, rescore, retry, second dispatch, nonce reuse or post-outcome protocol repair was performed by Relay.

## Consumed identity / exact refs

Fresh consumed FORMAL identity: `h7-r5-285a3a206b34c5982b9d4045`.

- binding SHA-256: `285a3a206b34c5982b9d404599aa272019dd9d4dceb661b49c97fd8750fd30d3`
- STARTED/control ref: `control/h7-r5-h7-r5-285a3a206b34c5982b9d4045-started@52b17b785364f96cc2e95507b2336252459d5352`
- preserve ref: `preserve/h7-r5-h7-r5-285a3a206b34c5982b9d4045-raw@a5e76e7eb117e0270cfdc138fb9da30d696aa7c0`
- freeze tag: `freeze/h7-r5-h7-r5-285a3a206b34c5982b9d4045-raw@a5e76e7eb117e0270cfdc138fb9da30d696aa7c0`
- formal tag: `formal/h7-r5-h7-r5-285a3a206b34c5982b9d4045@e6c4ec404b6264ccf8aa7e61eb69708e3b8cdc85`
- sealed tag: `sealed/h7-r5-h7-r5-285a3a206b34c5982b9d4045@e6c4ec404b6264ccf8aa7e61eb69708e3b8cdc85`
- evidence tag: `evidence/h7-r5-h7-r5-285a3a206b34c5982b9d4045@e6c4ec404b6264ccf8aa7e61eb69708e3b8cdc85`
- preserved raw SHA-256: `2c001b9893a3d6d3410800824ca2c11df5329f56abd8c419278dcdde6eae1112`
- official score blob: `d1604868f64db771d9a8c80f637b733607cde547`

R114 observed 7 official consumed identities before this FORMAL action; this run adds exactly one newly STARTED/sealed H7 identity. Relay records the post-run observed count as `8` and does not create or consume any additional identity.

## Result / evidentiary status

The sealed `official_score.json` records the decision exactly as `INCONCLUSIVE` under contract `H7-FORMAL-R1-DYNAMIC-TOP1-CONFIRMATORY-CONTRACT-DESIGN-V1` and evaluator `H7-FORMAL-R1-EVALUATOR-SPEC-V1`.

Observed exact boolean result fields are unchanged from the sealed score:

- `effect_reproduced`: dense `false`, eligibility `false`, fsa `false`
- `effect_conclusively_smaller`: dense `false`, eligibility `false`, fsa `false`
- `capacity_adequate`: dense `false`, eligibility `false`, fsa `false`

Relay does not reinterpret, rescue, retune, rescore or change any threshold/comparator/protocol based on this result. The prior scientific results and historical PASS/FAIL records remain unchanged.

- new scientific result this Relay generation: `true` (new externally produced sealed FORMAL score observed)
- evidentiary status: `FORMAL_CONSUMED_RESULT_SEALED_AWAITING_FRESH_ANALYST`
- science-affecting change by Relay: `false`
- prior-result preservation: `true`
- protected/held-out result newly accessed by Relay beyond the sealed official score: `false`
- consumed identity rerun/retune/rescore: `false`

## Funnel v2.1 preservation

Relay does not reinterpret R114's Funnel fields despite the completed FORMAL run. Until a fresh Evidence Analyst generation changes them, they remain exactly:

- claim_ceiling: `MECHANISM`
- preformal_eligible: `true`
- preformal_readiness: `READY`
- hold_class: `null`
- hold_reason: `null`
- terminal_state: `ACTIVE`
- queue_state: `QUEUED`
- system_priority_exception: `false`
- development_phase: `RESULT_EXPOSED_DEVELOPMENT`
- development_revision: `R5_UNCHANGED`

The workflow's consumed identity/result is recorded separately; Relay does not promote, terminate, reopen or revise H7 itself.

## Integrity

- Analyst R114 head re-read and still current immediately before mailbox mutation: `true`
- MAIN lease/state re-read; fresh PRIMARY RUNNING collision: `false`
- frozen science commit directly re-fetched: `true`
- controller commit directly re-fetched: `true`
- workflow run attempt: `1`; completed successfully
- STARTED identity binding matches R114 Analyst commit, controller and frozen science: `true`
- preserve branch and freeze tag resolve to the same preserve commit: `true`
- formal/sealed/evidence tags resolve to the same scored result commit: `true`
- preserve manifest asserts `preserve_before_target_access=true`: `true`
- workflow job order confirms raw preserve before target-side scoring: `true`
- immutable/formal/sealed/evidence/freeze/preserve refs mutated by Relay: `false`
- historical PASS/FAIL rewritten: `false`
- development phase/revision changed by Relay: `false`
- FORMAL hard floor respected by Relay: `true`

## Stop reason / next MAIN action

Stop reason: `WAITING_FRESH_EVIDENCE_ANALYST_POST_FORMAL_CONSUMPTION_AND_INCONCLUSIVE_RESULT`.

A fresh Evidence Analyst must now independently re-fetch the consumed identity, STARTED/preserve/freeze/formal/sealed/evidence refs, exact sealed score and current Funnel state, then issue the next canonical decision. Until that generation exists, MAIN/Relay must not re-arm, redispatch, retry, rerun, retune, rescore, repair the consumed identity, change scientific thresholds/comparators/protocol, or create a successor. The next MAIN action is only to consume that fresh Analyst decision when available.
