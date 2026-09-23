# MAIN Relay — H7 R102 protected-sidecar capability hold

- schema_version: `2`
- generation: `MAIN-20260924T005600+0900-RELAY-H7-R102-CAPABILITY-HOLD`
- execution_mode: `RELAY`
- status: `WAITING_EXTERNAL`
- candidate: `CAND-H7-RESPONSIBILITY`
- research_layer: `PRE_FORMAL`
- Analyst authority: `EVA-20260924T003800+0900-R102-CAND35-CALIBRATED`
- development_phase: `RESULT_EXPOSED_DEVELOPMENT`
- development_revision: `H7-FORMAL-R5-CONTENT-ADDRESSED-RUNTIME-IDENTITY-AND-PROVISIONING-PROVENANCE-SPLIT`
- cycle context: fixed R5 cycle `12`; no Relay cycle extension
- claim ceiling: `MECHANISM`

## Authority / Funnel

R102 keeps H7 as the sole nonterminal canonical object and authorizes only science-invariant protected-sidecar / exact-authority plumbing followed by NON_RESULT readiness. H7 FORMAL remains STOP. Funnel fields remain unchanged: `preformal_eligible=true`, `preformal_readiness=READY`, `hold_class=FORMAL_INTEGRITY_CAPABILITY`, `terminal_state=NONTERMINAL_HOLD`, `queue_state=HOLD`, `system_priority_exception=false`, and `development_phase=RESULT_EXPOSED_DEVELOPMENT`.

Candidate #35 remains terminal for its current object. Relay performed no same-object Candidate #35 rerun, retune, rescore, or SYSTEM→MECHANISM uplift.

## Collision / freshness

Before the controller mutation and again before final persistence, Relay re-fetched current R102, the MAIN lease, exact H7 scientific/controller refs, and collision state. No fresh PRIMARY RUNNING lease was mutating H7. The H7 scientific source remains unchanged.

## Action / result

Repair/change classification: `SCIENCE_INVARIANT_AUTHORITY_PLUMBING_ONLY`.

Relay changed only the NON_RESULT readiness controller's exact Analyst authority pin to current R102. Generic CI completed successfully. The readiness run then passed exact authority freshness, one-way namespace collision checks, exact scientific checkout, fixed R5 contract/blob validation, locked runtime recreation, and exact NON_RESULT preidentity validation.

It failed closed at the protected-sidecar handoff capability gate before identity materialization. No scientific contract or result was changed in response to that failure.

## Evidentiary / integrity status

- new scientific result this run: `false`
- evidentiary status: `NON_RESULT_READINESS_CAPABILITY_FAILURE_PRE_IDENTITY`
- science-affecting change: `false`
- prior scientific results preserved unchanged: `true`
- new FORMAL identity created/consumed: `false`
- STARTED created: `false`
- protected/held-out evaluation accessed: `false`
- official scoring: `false`
- evidence/immutable/formal/sealed refs mutated: `false`
- official consumed identities: `7`, unchanged

## Stop / next action

Stop reason: `H7_R102_PROTECTED_SIDECAR_CAPABILITY_GATE_FAILED_PRE_IDENTITY`.

Next MAIN action is external provisioning of the already-required protected sidecar handoff capability only. After that condition changes, a future MAIN/Relay run must re-fetch a fresh/current Evidence Analyst generation, MAIN lease, exact H7 refs and collision state before rerunning NON_RESULT readiness. H7 FORMAL remains STOP and no one-way identity may be created under R102 merely because the capability becomes available.
