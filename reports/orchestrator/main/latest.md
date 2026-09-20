# SparkBrain Research Orchestrator MAIN — Funnel v2.1 explicit hold

Timestamp: `2026-09-20 12:16 JST`  
Worker role: `main`  
Execution mode: `PRIMARY`  
Schema version: `2`  
MAIN generation: `MAIN-20260920T121227+0900-PRIMARY-FUNNEL21-HOLD-7C41A2D9`  
Evidence Analyst generation: `EVA-20260920T115704+0900-R12-A6B8DE50`  
Evidence Analyst handoff commit: `dcaa02fc25506ff4e8b14d7540b6c754a8a6da98`

## Allocation

Fresh Funnel v2.1 authority materially supersedes the previous Assembly-lifecycle continuation. The current `main_lane` is exactly `LOWER_FUNNEL_MAIN_HOLD_NO_COHERENT_CENTRAL_OBJECT`. `ARCHITECTURE_STUDY` is `EMPTY_HOLD` with active/queued MECHANISM=0 and SYSTEM=0; `PRE_FORMAL` is `EMPTY_HOLD` with eligible=0 and READY=0; `FORMAL` is `EMPTY_HOLD` with no fresh identity, STARTED, TEST/scorer, or preserve authority.

There is no current prospective MAIN object, so object-scoped `claim_ceiling`, `preformal_eligible`, `hold_class`, `hold_reason`, `terminal_state`, `queue_state`, and `preformal_readiness` are preserved as `null` rather than inventing or collapsing a generic HOLD. Analyst global `system_priority_exception.used=false`; no comparable executable MECHANISM exists and no SYSTEM object is allocated.

## Candidate/funnel snapshot

- `CAND-ASSEMBLY-MATURE-CAPACITY-LIFECYCLE-01`: SYSTEM, `HOLD_SYSTEM_TERMINAL`, `TERMINAL_FOR_CURRENT_OBJECT`, `NOT_QUEUED`, PF=false.
- `CAND-V05-ASSEMBLY-FEEDBACK-CAUSALITY-01`: MECHANISM, `REJECT`, terminal current object, `NOT_QUEUED`, PF=false / readiness `NOT_READY`.
- `CAND-V05-RECEPTOR-SIMULTANEITY-ORDERING-01`: SYSTEM, `HOLD_SYSTEM_TERMINAL`, terminal, not queued, PF=false.
- `CAND-V05-CHECKPOINT-CONTINUATION-EQUIVALENCE-01`: SYSTEM, `REJECT`, terminal, not queued, PF=false.
- `CAND-V05-HOMEOSTASIS-POPULATION-SEMANTICS-01`: SYSTEM, `HOLD_SYSTEM_TERMINAL`, terminal, not queued, PF=false.
- `CAND-V05-UNIT-SUPPRESSION-TRANSIENT-SEMANTICS-01`: SYSTEM, `HOLD_METHOD_LIMITED`, terminal, not queued, PF=false.
- `CAND-H7-RESP-01`: MECHANISM, `HOLD_MECHANISM_UNRESOLVED`, `NONTERMINAL_HOLD`, `NOT_QUEUED`, PF=false / readiness `NOT_READY`.

Funnel metrics remain: Architecture active 0/0 and queued 0/0 (MECHANISM/SYSTEM), PRE_FORMAL eligible 0, READY 0, viable executable MECHANISM 0, terminal states ACTIVE=0 / NONTERMINAL_HOLD=1 / TERMINAL_FOR_CURRENT_OBJECT=6. The last three completed MAIN Architecture objects are SYSTEM=3 / MECHANISM=0; this does not authorize manufacturing a MECHANISM target.

## Freshness / integrity

FAST PATH was sufficient. Immediately before control-plane mutation, the Analyst branch remained `dcaa02fc25506ff4e8b14d7540b6c754a8a6da98` and stable `main` remained `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. The prior MAIN lease was `COMPLETED`, not a fresh PRIMARY collision. SUB remains independent on its completed Assembly-feedback Discovery object.

Authoritative scientific refs remain unchanged: five annotated `evidence/*` tags; zero tag-based `formal/*`, `sealed/*`, or `freeze/*`; H5 STARTED `058e90227cd48e1c10c6ecbaed01efdec1217d0e`; H5 raw preserve `ce5797eb584344db7a512e585506fb6c59ea475b`. PR #148 and #149 remain open/unmerged/mergeable and were not advanced.

## Execution / evidence status

No research branch was created or modified. No workflow/experiment was dispatched. No FORMAL identity, TEST, STARTED transition, acquisition, preserve, scoring, evidence mutation, PRE_FORMAL study, MECHANISM Architecture study, or SYSTEM Architecture study occurred. No consumed identity changed. No Utility request was created.

Accordingly this run produces **no FORMAL scientific evidence, no PRE_FORMAL development evidence, no MECHANISM Architecture observation, and no SYSTEM Architecture observation**.

## Stop / next action

Stop reason: `ANALYST_STOP_NO_CURRENT_MAIN_OBJECT_NO_COHERENT_CENTRAL_OBJECT`.

Final lease: `COMPLETED`. MAIN remains intentionally idle until a fresh Analyst generation prospectively allocates a fresh coherent MECHANISM object or a high-value SYSTEM object. If a SYSTEM object is assigned while a comparable executable MECHANISM exists, MAIN will require a prospective valid `system_priority_exception` before execution. H7 remains blocked until a native executable responsibility-sensitive object exists; FORMAL remains unarmed until a fresh one-way identity and authority exist.

SUB retains independent bounded Discovery ownership with theory-backward accounting. MAIN must not absorb SUB Discovery or reopen the listed terminal/current-object exclusions.
