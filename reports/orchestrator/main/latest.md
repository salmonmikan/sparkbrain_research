# MAIN latest — candidate #34 PRE_FORMAL R2

- execution_mode: `RELAY`
- status: `BLOCKED`
- layer: `PRE_FORMAL`
- cycle: 4
- development_phase: `OPEN_DEVELOPMENT`
- development_revision: `PRE_FORMAL-R2-OPPORTUNITY-AWARE-VERSIONED-REVISION-AUTHORIZED`
- claim_ceiling: `MECHANISM`
- preformal_eligible: `true`
- preformal_readiness: `NOT_READY`
- terminal_state: `NONTERMINAL`
- queue_state: `QUEUED_FOR_MAIN_PREFORMAL_R2_OPPORTUNITY_AWARE_CONTRACT_REVISION_NONRESULT`
- system_priority_exception.used: `false`

The exact-head generic CI and dedicated R2 non-result contract workflow both completed successfully. No response-bearing execution occurred.

Relay then re-fetched the canonical Evidence Analyst branch before durable capture. The commit referenced by PRIMARY currently resolves to Analyst generation `EVA-20260923T105725+0900-R92-6B8E31D4` with the opportunity-aware R2 revision above, while PRIMARY and the generated R2 contract are bound to `EVA-20260923T110053+0900-R92-A7B61F3C` and a different revision description. The generated contract hard-codes that mismatching authority identity.

Because durable capture would preserve a contract bound to a generation/revision that does not match the canonical Analyst content, Relay failed closed. It did not rewrite the authority, did not reinterpret the R2 revision, did not modify the research branch, and did not dispatch any response-bearing or FORMAL work.

D34-Q001 and all prior results remain unchanged. Next action is a fresh Evidence Analyst or PRIMARY reconciliation that explicitly binds the exact R2 branch/contract to current authority before durable capture or execution.
