# MAIN RELAY R129 — Theory R4 observed; waiting for Evidence Analyst classification

Execution mode: `RELAY`  
Status: `WAITING_EXTERNAL`  
Canonical MAIN object: `NONE_ALLOCATED`  
Evidence Analyst authority: `EVA-20260924T211100+0900-R125-HUMAN009-R62-NO-CANONICAL-ADMISSION`  
Supersedes MAIN generation: `MAIN-20260924T212000+0900-PRIMARY-R128-R125-HUMAN009-NO-CANONICAL-ACTION`

## Relay action

Re-fetched the current Evidence Analyst generation, current MAIN generation/lease, stable `main`, and the directly related H7 scientific/controller refs. No fresh PRIMARY RUNNING lease exists on an allocated scientific object, and no scientific object is currently allocated by Evidence Analyst R125.

A newer noncanonical Theory synthesis was then observed at commit `42165c89b0072c26258c7d6c09949bc487a3c24e`: generation `THEORY-20260924T213041+0900-R4-ANONYMOUS-LINEAGE-ADDRESSABILITY-6B2D9F41`, proposal `TH-002-ANONYMOUS-LINEAGE-ADDRESSABILITY`. The Theory artifact explicitly declares zero execution authority, no Revisit proposal, and requires a later Evidence Analyst gate before any Forge or MAIN execution.

Relay therefore performed **control-state reconciliation only**. It did not adopt, score, operationalize, implement, tune, or execute TH-002. No candidate ID, development phase/revision, Funnel typing, identity, scientific threshold, comparator, intervention, resource contract, falsifier, or success criterion was created or changed. The proposal is recorded only as a pending external/noncanonical input awaiting Evidence Analyst classification.

## Development / Funnel preservation

Current no-object fields are preserved exactly from MAIN R128:

- `candidate_id`: `null`
- `research_layer`: `null`
- `claim_ceiling`: `null`
- `preformal_eligible`: `null`
- `preformal_readiness`: `null`
- `hold_class`: `null`
- `hold_reason`: `null`
- `terminal_state`: `NO_ALLOCATED_ACTIVE_OBJECT`
- `queue_state`: `EMPTY`
- `system_priority_exception`: `null`
- `development_phase`: `null`
- `development_revision`: `null`
- `cycle_count`: `25`
- cycle/reassessment context: `NO_SCIENTIFIC_CYCLE_EXTENSION_OR_REASSESSMENT_EXECUTION`

Canonical funnel totals remain unchanged: 35 canonical objects = 14 MECHANISM / 21 SYSTEM; 35 terminal; 0 active; 0 scientifically queued; 0 effectively executable MECHANISM; 8 consumed identities.

## Formal floor / prior-result preservation

H7 remains terminal `FORMAL / MECHANISM / CONSUMED_ONE_WAY / R5_UNCHANGED / INCONCLUSIVE`. Its consumed identity `h7-r5-285a3a206b34c5982b9d4045` was not rerun, retuned, rescored, repaired, or reopened. No immutable/formal/sealed/evidence ref was mutated. Current directly re-fetched H7 research refs remain:

- scientific branch `research/main-h7-formal-r5-runtime-identity-r88-cycle12` → `2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`
- controller branch `research/main-h7-r5-launch-plumbing-r111-workflow-dispatch` → `af3aa97574c365e3e918c3d4d012faa4886760d0`

Candidate #35 remains terminal SYSTEM with zero confirmatory credit, no active Revisit trigger, no fresh successor, and no MAIN execution authority. No historical PASS/FAIL or INCONCLUSIVE result was reinterpreted.

## Freshness / collision / integrity

Immediately before persistence:

- Evidence Analyst handoff remained `918d804f8d66a7463678b79621266045949045f4` (R125).
- MAIN report branch remained `d4f905c36d54e21023524420139dee334523cd2a` at the start of this persistence sequence.
- stable `main` remained `d16403414fc7abebd23075fc401240971b8eb91d`.
- current MAIN lease was not a fresh PRIMARY RUNNING same-object lease; it was a stopped/no-allocated-object R128 state.
- no protected evaluator or held-out data was accessed.
- no scientific scoring or scientific workflow dispatch occurred.

Repair/change classification: `CONTROL_STATE_RECONCILIATION_ONLY`.  
Science-affecting change: `false`.  
Science-invariant scientific repair: `false`.  
Evidentiary status: `NOT_EVIDENCE`.  
New scientific result: `false`.  
Prior scientific results preserved unchanged: `true`.

## Waiting condition and next MAIN action

Pending external/noncanonical input:

- type: `NONCANONICAL_THEORY_PROPOSAL`
- generation: `THEORY-20260924T213041+0900-R4-ANONYMOUS-LINEAGE-ADDRESSABILITY-6B2D9F41`
- proposal: `TH-002-ANONYMOUS-LINEAGE-ADDRESSABILITY`
- source commit: `42165c89b0072c26258c7d6c09949bc487a3c24e`
- scientific execution authority: `NONE`
- MAIN may execute it now: `false`

There is no result-bearing workflow to poll; workflow id is `null`. The exact next action is to wait for a **later Evidence Analyst generation** that explicitly classifies this Theory proposal. MAIN may continue only if that later Analyst generation prospectively admits and allocates a concrete scientific object/identity with the required Funnel/development fields and explicit authority. If it rejects, defers, or leaves the proposal noncanonical, preserve current science and remain stopped/waiting.

Stop/wait reason: `WAITING_FOR_EVIDENCE_ANALYST_CLASSIFICATION_OF_NONCANONICAL_THEORY_R4_TH002`.
