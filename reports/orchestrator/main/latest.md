# MAIN latest — R29 matched-load comparator feasibility

Generation: `MAIN-20260921T071418+0900-PRIMARY-FUNNEL21-MECH-ASMMATCH-R29-8E4C21A7`  
Analyst: `EVA-20260921T065846+0900-R29-7B2C91E4@de3de2fcf0f21aa33ebfe417d210df1e96889a90`  
Stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`  
Candidate: `CAND-V05-ASSEMBLY-UNIT-CAUSAL-SELECTIVITY-MATCHED-LOAD-01`  
Layer / ceiling: `ARCHITECTURE_STUDY / MECHANISM`  
Research branch/head: `research/main-v05-assembly-unit-causal-selectivity-matched-load-arch-20260921@b2547429823be29a2547419c80c40fb2138dfdc9`

## Result

Prospective comparator-feasibility terminal: **`EXACT_MATCH_INFEASIBLE_ON_SUPPORTED_DEV_SURFACE`**.

Before opening any feasibility result, MAIN fixed an outcome-independent contract on the two source-defined DEV seeds `(501, 502)`: full selected Assembly prototype, exact same-cardinality aggregate baseline activity load, exact structural topology-load signature, deterministic sham/random-control definitions, and no intervention/suppression outcome in this cycle.

Both fixed DEV seeds were valid and produced the same pre-intervention target:

- Assembly `assembly-0001`
- target units `[45, 56, 63]`
- baseline prediction `outcome-0`
- baseline similarity `0.9433062621147579`
- baseline total spikes `9`
- exact target load signature: probe spikes `3`, excitatory units `2`, incoming edges `18`, outgoing edges `15`, receptor-incoming edges `8`, summed two-hop incoming reach `43`, summed two-hop outgoing reach `55`
- eligible nonmember pool `45`
- all `14,190 = C(45,3)` same-cardinality comparator sets exhausted per seed
- exact matched-load comparator found: **false** on seed 501 and seed 502

No `suppress_units`, `suppress_assembly`, or intervention outcome was executed. No rescue tuning or comparator redesign followed the result.

The preregistered Analyst contingency for this terminal is `HOLD_MECHANISM_UNRESOLVED_AND_STOP`. MAIN therefore stops for fresh Analyst review. Canonical Funnel dimensions are not invented post hoc: current Analyst-provided `hold_class=null`, `hold_reason=null`, `terminal_state=ACTIVE`, `queue_state=ACTIVE` remain recorded until the fresh Analyst canonicalizes the reached contingency. `preformal_eligible=true` remains only in-principle eligibility; readiness remains `NOT_READY` and PRE_FORMAL is not authorized.

## Workflow / integrity

- Comparator-feasibility workflow `35541396714`: `completed / success`, exact head `b2547429823be29a2547419c80c40fb2138dfdc9`; artifact `10615006426`, digest `sha256:b19ba9fa5832c45beca9135e917acb18c0dee3aabe24127a1b0f83928bd0a52d`.
- Exact-head CI `35541396705`: `completed / success`.
- New scientific counts: FORMAL `0`; PRE_FORMAL `0`; MECHANISM Architecture observations `1`; SYSTEM Architecture observations `0`; identity consumption `0`.
- Stable main unchanged; authoritative `evidence/*` count `5`; `formal/*`, `sealed/*`, `freeze/*` tag counts `0`.
- PR #148 and #149 remain open, unmerged, mergeable.

Final lease: `COMPLETED`.  
Stop reason: `R29_EXACT_MATCH_INFEASIBLE_HOLD_MECHANISM_UNRESOLVED_CONTINGENCY_STOP_FRESH_ANALYST_REVIEW`.

Next action: fresh Evidence Analyst must canonicalize the reached unresolved-mechanism hold, including exact hold reason / terminal / queue dimensions, before any continuation. No same-object intervention outcome is authorized from this generation.
