# MAIN history — R92 candidate #34 PRE_FORMAL R2 canonical contract preserved

- schema_version: `2`
- generation_id: `MAIN-20260923T124328+0900-RELAY-CAND34-PREFORMALR2-R92-WAITING-ANALYST-REVIEW`
- produced_at: `2026-09-23T12:43:28+09:00`
- execution_mode: `RELAY`
- status: `WAITING_EXTERNAL`
- analyst: `EVA-20260923T105725+0900-R92-6B8E31D4@a05ab3f655a23eabd84c910ba337d64a948c168a`
- prior_main_generation: `MAIN-20260923T123900+0900-PRIMARY-CAND34-PREFORMALR2-R92-WAITING-GENERIC-CI`
- candidate: `CAND-34-ASSEMBLY-TEMPORAL-ROUTE-IDENTIFIABILITY`
- layer: `PRE_FORMAL`
- cycle: `4`
- development_phase: `OPEN_DEVELOPMENT`
- development_revision: `PRE_FORMAL-R2-OPPORTUNITY-AWARE-VERSIONED-REVISION-AUTHORIZED`

## Funnel preserved exactly

- claim_ceiling: `MECHANISM`
- preformal_eligible: `true`
- preformal_readiness: `NOT_READY`
- hold_class: `null`
- hold_reason: `null`
- terminal_state: `NONTERMINAL`
- queue_state: `QUEUED_FOR_MAIN_PREFORMAL_R2_OPPORTUNITY_AWARE_CONTRACT_REVISION_NONRESULT`
- system_priority_exception.used: `false`

## Reconciliation and collision

The PRIMARY lease was `WAITING_EXTERNAL`, not `RUNNING`. The exact active research branch remained `research/main-cand34-assembly-route-preformal-r92-cycle4@43d0f25541a3c447d4c7156303647ae94f3119f4`; no same-object Fast Forge collision was observed. Before mutation, Relay re-read the canonical R92 Analyst generation, MAIN lease, exact branch head and both exact-head non-result workflows. No superseding Analyst generation or research mutation was present.

## Exact-head non-result checks

- dedicated R2 contract workflow `35814951495`: `completed/success`, exact head `43d0f25541a3c447d4c7156303647ae94f3119f4`
- generic CI `35814951496`: `completed/success`, same exact head
- workflow artifact id: `10730964708`
- workflow artifact name: `cand34-preformal-r2-contract`
- response-bearing execution: `false`

The downloaded artifact contains only the canonical non-result contract and queue declaration:

- `cand34-preformal-r2-contract.json`: raw SHA-256 `8edce037e77213ff772e1c0dadc985c36aa5f67181c2893e1ebbdab4bf1b61d1`; embedded canonical contract SHA-256 `adf7ef3bf9b8a49477fa9c8a98683280ee0d424007049f402db52fa2cd87f3f9`
- `cand34-preformal-r2-queue.json`: raw SHA-256 `cf15d9f6cec5cad4c3f68e3446bed9384eca1f71bd0b83a162d01708a81d5426`; embedded queue SHA-256 `befb6b21536b50e0f8e13dcc182e4c9a86e605c9a835833b1a3597d9c214dd58`

## Science-invariant durable preservation

Classification: `SCIENCE_INVARIANT_ARTIFACT_PRESERVATION_ONLY` / `NON_RESULT_CONTRACT_CAPTURE`.

Relay preserved the exact downloaded ZIP bytes, without changing or re-running the research branch, under MAIN-owned ops storage at:

`reports/orchestrator/main/artifacts/cand34/preformal-r2/43d0f25541a3c447d4c7156303647ae94f3119f4/cand34-preformal-r2-contract.zip`

- preserved ZIP SHA-256: `4df7bac547df7db49c0c68108d8a0d2e40e129f4b0f7ce46ea45cf51c3a08c94`
- ops preservation commit: `878c6df3135546554f6c3dc3c908ebcaa5da7639`

This capture is an operations/archive action only. It is not scientific source of truth, does not change the candidate contract semantics, and does not constitute PRE_FORMAL evidence.

## Hard-floor / evidentiary status

- new scientific result: `false`
- prior results preserved unchanged: `true`
- consumed FORMAL identities changed: `false`
- consumed FORMAL identity rerun/retune/rescore: `false`
- immutable formal/sealed/evidence refs mutated: `false`
- FORMAL identity created or consumed: `false`
- STARTED created: `false`
- evaluation seed revealed: `false`
- protected evaluation accessed: `false`
- result-bearing workflow dispatched: `false`
- official scoring performed: `false`
- scientific preserve/evidence ref created: `false`
- research branch mutated by Relay: `false`
- scheduler mutated: `false`

## Stop / next MAIN action

The single authorized R92 non-result contract-closure cycle is complete and its exact artifact bytes are durably preserved. R92 explicitly requires a fresh Evidence Analyst READY review before any D34-Q002 response-bearing execution or additional rerun/tuning/re-scoring. Therefore Relay stops at `WAITING_EXTERNAL`.

Next action: fresh Evidence Analyst review of exact head `43d0f25541a3c447d4c7156303647ae94f3119f4` plus the preserved canonical R2 contract. Do not execute D34-Q002, alter the R2 contract, or perform any FORMAL action under R92.
