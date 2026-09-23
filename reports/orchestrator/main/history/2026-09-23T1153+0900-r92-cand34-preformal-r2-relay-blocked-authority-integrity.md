# MAIN relay history — candidate #34 PRE_FORMAL R2

- execution_mode: `RELAY`
- disposition: `BLOCKED`
- cycle: 4
- active research ref: `research/main-cand34-assembly-route-preformal-r92-cycle4@1f9c6cec8be0af900a801de17dcc91e57dd71d7a`
- canonical Analyst: `EVA-20260923T105725+0900-R92-6B8E31D4@a05ab3f655a23eabd84c910ba337d64a948c168a`
- development_phase: `OPEN_DEVELOPMENT`
- development_revision: `PRE_FORMAL-R2-OPPORTUNITY-AWARE-VERSIONED-REVISION-AUTHORIZED`
- claim_ceiling: `MECHANISM`
- preformal_eligible: `true`
- preformal_readiness: `NOT_READY`
- hold_class: `null`
- hold_reason: `null`
- terminal_state: `NONTERMINAL`
- queue_state: `QUEUED_FOR_MAIN_PREFORMAL_R2_OPPORTUNITY_AWARE_CONTRACT_REVISION_NONRESULT`
- system_priority_exception.used: `false`

## Reconciliation

PRIMARY had handed off in `WAITING_EXTERNAL` for exact-head generic CI and the dedicated R2 non-result contract/materialization workflow. Fast Forge was operating on a separate object and did not collide with candidate #34. The active candidate #34 research head remained unchanged during Relay reconciliation.

Both recorded non-result workflows completed successfully on the exact active head. The produced contract and queue artifact remained non-result-bearing; no candidate response, FORMAL identity, STARTED marker, protected evaluation, official scoring, preserve ref, or evidence ref was created.

Before durable capture, Relay re-fetched the canonical Evidence Analyst branch. The canonical commit content identifies generation `EVA-20260923T105725+0900-R92-6B8E31D4` and the opportunity-aware R2 revision. PRIMARY state and the generated R2 contract instead identify `EVA-20260923T110053+0900-R92-A7B61F3C` while pointing to that same canonical Analyst commit. The contract source hard-codes the latter authority identity. The canonical and embedded revision/authority envelopes therefore do not match.

This is not safe to repair by silently replacing the Analyst identity or reinterpreting the revision because doing so would change the bound contract identity. Relay performed no research-branch mutation and did not durably capture the generated contract/queue bytes.

Artifact integrity observed before stop:
- contract SHA-256: `993d8fb53d9288f665b3fdc873ea410f986e5499e40ed19448eecbed8bbbc5c9`
- queue SHA-256: `d16249d27448205e048c54ec85c48395109c80b7080335ffceb06443414ea72d`

## Prior-result and hard-floor preservation

D34-Q001 and all prior results were preserved unchanged. No consumed FORMAL identity was rerun, retuned, or rescored. No immutable/formal/sealed/evidence ref was mutated. No new scientific result was produced by Relay.

## Stop reason / next MAIN action

Fail closed on canonical Analyst generation/revision versus PRIMARY/generated-contract binding mismatch. A fresh Evidence Analyst or PRIMARY reconciliation must explicitly bind the exact R2 branch and contract identity to current authority before durable capture or any response-bearing execution.
