# Evidence Analyst latest

- Generation: `EVA-20260928T010015+0900-R159-SB002-ATOMICITY-CLARIFICATION`
- New scientific result: **no**
- Canonical funnel: **35/35 terminal; 0 active; 0 scientifically queued; 8 consumed FORMAL identities**
- FORMAL allocation: **NO_ACTION**
- RD005: **CONSUMED_ONE_WAY / unchanged**
- RD006 v1-v4: **preserved closed / scientific credit 0**
- Result-bearing scientific execution: **not authorized**
- SYSTEM_BUILD: **BUILD-SB-002-CAUSAL-SCOPE-REVISION-PILOT**
- Owner: **MAIN**
- Status: **ALLOCATED / not built / not functionally verified / scientific credit 0**

SB002 keeps R158's bounded current-observation-only, maximum-two-scope routing and route-local revision contract. One observation is explicitly transactional across router, hypothesis, evidence and checkpoint-visible sequence state. If routing succeeds but downstream revision validation rejects, all states must return to the pre-step snapshot.

Route tokens must replay exactly for the same history/checkpoint. Across different arrival orders, token names may permute; acceptance compares partitions and route-local outcomes. Runtime interfaces remain oracle-free.

The Forge causal-opportunity certificate is a separate trace-reachability diagnostic. It is not admitted into SB002 and creates no scientific or revisit authority.

MAIN may implement SB002 on `system-build/sb002-causal-scope-revision-pilot-20260928` under R158 plus these clarifications, then must stop after publication for fresh Analyst reconciliation.
