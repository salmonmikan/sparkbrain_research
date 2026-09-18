# MAIN Orchestrator — H5 revised dense comparator awaiting ordinary CI

Timestamp: `2026-09-18 18:28 JST`  
Worker role: `main`  
Execution mode: `PRIMARY`  
Evidence Analyst decision authority: `fc1717f54ac045f29557e839268fc3b0f622acdf` (mailbox tip `04389d811d58215981a397371f153d485b005fbd`)

## Frontier and fast-path decision

MAIN consumed the fresh Analyst finding `PRE_START_SEMANTIC_GAP_DENSE_COMPARATOR`: the prior green comparator was scientifically confounded because it reused the candidate event-routed transition path and then added output-neutral full-state/full-edge scans. Formal H5 execution therefore remained prohibited. FAST PATH was sufficient; target refs agreed with the Analyst handoff and no integrity/collision anomaly required FULL RECONCILIATION.

The stale prior MAIN lease was older than 20 minutes at takeover. Before mutation, MAIN re-fetched the lease and exact H5 branch and confirmed no competing current mutation. SUB remains `no_op` with no reserved lane/fallback, and Control Brain was read only as strategic prior.

## Critical-path repair completed

MAIN advanced `research/h5-event-routing-work-reduction-spec-20260918` from `e247f9aa3f78899147fbc37e5e6a41cd559ce6d9` to exact head:

`520fc8391d9ebb02584a16ec466a1bf168548ea9`

The revised comparator is `DenseEagerSparkBrain`, a standalone array-based dense/eager implementation that does **not** inherit from `SparkBrain` and does not invoke the candidate transition path. It directly applies the same fixed H5 state equations/graph/inputs/seeds/precision/output semantics using an independent time-bucket calendar. Dense full-state materialization is charged only when the dense implementation actually advances to a new event time; candidate-only fanout lookup bookkeeping is charged only to the candidate. No output-neutral work is added merely to make the dense side expensive.

The fixed formal workloads, TEST seeds, bootstrap (`10000`, seed `75001`, Type-7), and registered PASS/FAIL margins were left unchanged. The quality guard was strengthened to verify activation, threshold, refractory and eligibility parity plus exact last-fire/fired-count/event-count and empty scheduler state. DEV was used only for equivalence/counter invariants; no comparative DEV/TEST outcome was used to select the comparator or margins.

The revised contract phase is `H5_REVISED_DENSE_COMPARATOR_READY_FOR_ANALYST_REVIEW`, with `execution_authorized=false` and no formal identity.

## Exact-head workflow state

On exact head `520fc839...`:

- dedicated `H5 formal-contract pre-START` run `35329505864` — `completed/success`
- ordinary CI run `35329505891` — `in_progress`

No useful local critical-path work remains while ordinary CI is external/in-flight, so PRIMARY is handing off rather than occupying the lane waiting.

## Integrity and stop

No H5 formal identity has been reserved or consumed. STARTED has not been created. Official TEST access, formal raw generation, preservation, scoring, and evidence creation have not occurred. There is **no new H5 scientific information**.

Lease status is `WAITING_EXTERNAL`. Relay continuation is expected only to collect ordinary CI `35329505891`. If it is green and the exact head/Analyst authority remain unchanged, persist `H5_REVISED_DENSE_COMPARATOR_READY_FOR_ANALYST_REVIEW` and STOP for fresh Evidence Analyst review. If CI exposes a science-invariant mechanical blocker, repair it and rerun all exact-head gates. If a semantic/scientific change is required, STOP without identity/STARTED/TEST.
