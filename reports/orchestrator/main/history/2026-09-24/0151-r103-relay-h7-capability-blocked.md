# MAIN Relay — H7 R103 protected-sidecar capability blocked

- schema_version: `2`
- generation: `MAIN-20260924T015100+0900-RELAY-H7-R103-CAPABILITY-BLOCKED`
- execution_mode: `RELAY`
- status: `BLOCKED`
- candidate: `CAND-H7-RESPONSIBILITY`
- research_layer: `PRE_FORMAL`
- Analyst authority: `EVA-20260924T010800+0900-R103-FORGE-DEFER-SCHEDULER-RED`
- prior MAIN generation: `MAIN-20260924T014800+0900-RELAY-H7-R103-READINESS-WAITING`
- development_phase: `RESULT_EXPOSED_DEVELOPMENT`
- development_revision: `R5_UNCHANGED`
- scientific contract revision: `H7-FORMAL-R5-CONTENT-ADDRESSED-RUNTIME-IDENTITY-AND-PROVISIONING-PROVENANCE-SPLIT`
- cycle context: fixed authorized cycle `12`; Relay did not extend the scientific cycle

## Authority / Funnel

R103 authorizes only science-invariant protected-sidecar capability and exact-authority plumbing followed by strictly NON_RESULT readiness. H7 FORMAL remains STOP, and even a green readiness would require a fresh Evidence Analyst generation before any one-way FORMAL action.

Funnel fields are preserved exactly from R103: `claim_ceiling=MECHANISM`, `preformal_eligible=true`, `preformal_readiness=READY`, `hold_class=FORMAL_INTEGRITY_CAPABILITY`, `hold_reason=Protected-sidecar handoff capability unavailable; latest NON_RESULT readiness failed before identity materialization.`, `terminal_state=NONTERMINAL_HOLD`, `queue_state=HOLD`, `system_priority_exception=false`, `development_phase=RESULT_EXPOSED_DEVELOPMENT`, `development_revision=R5_UNCHANGED`.

Candidate #35 remains terminal for its current SYSTEM object. No Candidate #35 rerun, retune, rescore, successor rescue, or SYSTEM-to-MECHANISM uplift occurred.

## Collision / freshness

Before mutation and again before final persistence, Relay re-fetched the current Evidence Analyst generation, MAIN state/lease, and exact H7 scientific/controller refs. The Analyst generation remained R103. MAIN was not a fresh PRIMARY RUNNING lease on the H7 object. Fast Forge had explicitly avoided H7 and reported no same-object collision. The exact H7 scientific source remained unchanged at `research/main-h7-formal-r5-runtime-identity-r88-cycle12@2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`.

## Action / result

Repair/change classification: `SCIENCE_INVARIANT_EXACT_AUTHORITY_PLUMBING_ONLY`.

Relay changed only the strictly NON_RESULT readiness workflow's exact Evidence Analyst pin from the superseded R102 generation to current R103. No hypothesis, metric/scorer meaning, scientific threshold/tolerance, comparator, seed/exclusion policy, intervention, resource/privilege contract, falsifier, success criterion, scientific source, or protected data was changed or accessed.

The controller head became `research/main-h7-r5-oneway-controller-r98@d610b18283953f21dfb27859f0d0b190d5f56a24`. Generic CI completed successfully. The exact R103-bound NON_RESULT readiness run completed with failure only at the protected-sidecar capability gate after the earlier exact-authority, untouched-namespace, exact-source, fixed-contract/blob, locked-runtime, and NON_RESULT preidentity checks had passed.

The failing gate reported that repository Actions secret `H7_R5_SIDECAR_PASSPHRASE` is missing. The workflow refused to arm FORMAL. This is an external capability/provisioning blocker, not a scientific outcome and not an authorized target for Relay to invent around.

## Evidentiary / integrity status

- new scientific result this run: `false`
- evidentiary status: `NON_RESULT_READINESS_CAPABILITY_GATE_FAILED_PRE_IDENTITY`
- science-affecting change: `false`
- prior scientific results preserved unchanged: `true`
- new FORMAL identity created/consumed: `false`
- STARTED created: `false`
- protected/held-out evaluation accessed: `false`
- official scoring: `false`
- historical PASS/FAIL rewritten: `false`
- evidence/immutable/formal/sealed/freeze/preserve refs mutated: `false`
- official consumed identities: `7`, unchanged

## Stop / next action

Stop reason: `H7_R103_PROTECTED_SIDECAR_CAPABILITY_MISSING`.

Next MAIN action: provision the protected-sidecar handoff capability outside Relay by supplying the repository Actions secret `H7_R5_SIDECAR_PASSPHRASE` under the intended security boundary. After that external capability exists, a later relay/PRIMARY run may re-fetch current Analyst/Main authority and run only the exact prospectively authorized NON_RESULT readiness. No FORMAL identity creation, STARTED marker, result-bearing evaluation, or scoring is authorized under R103.
