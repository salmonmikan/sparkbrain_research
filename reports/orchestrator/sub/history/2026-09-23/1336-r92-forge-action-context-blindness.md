# FAST FORGE — context-conditioned action formation probe

- schema_version: `2`
- generation_id: `FORGE-20260923T133600+0900-ACTION-CONTEXT-DEADEND-R92`
- produced_at: `2026-09-23T13:36:00+09:00`
- worker_role: `FAST_FORGE`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- overall_status: `FORGE_DEAD_END`

## Freshness / ownership

Re-fetched canonical and operational surfaces before work. Evidence Analyst remains R92 at `a05ab3f655a23eabd84c910ba337d64a948c168a`; stable main remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. MAIN candidate #34 is owned on `research/main-cand34-assembly-route-preformal-r92-cycle4`, currently observed at `43d0f25541a3c447d4c7156303647ae94f3119f4`. No Relay branch was observed. Recent Literature R36, Independent Audit R8, Methodology R81 and Utility PF-R1 pointer-divergence state were re-read; they remain centered on candidate #34/H7 and do not allocate an action-policy Forge object.

Forge explicitly excluded candidate #34 route/opportunity/scorer/runtime/workflow surfaces, candidate #35 queue-free physical-state surface, H7 FORMAL/provenance/preservation, all consumed/frozen identities, and historical action-delay/nonlearning-visit objects.

Two tempting alternatives were rejected before execution as duplicates/rescue-like work: receptor/hash route aliasing already has `research/exploratory-sub-topology-fanout-aliasing-20260920`; native responsibility/credit has a dense retained family of responsibility/credit/replay/topology/eligibility studies. No mutation was made for either.

## Forge object — same-Assembly context-sensitive action meaning

- forge_id: `FORGE-ACTION-CONTEXT-BLINDNESS-A`
- question: Can one mature Assembly acquire different functional actions in two external contexts when the context does not alter Assembly identity or enter the action-policy state?
- why_now: This is a bounded pre-semantic->functional formation question independent of MAIN route causality and distinct from the prior predictor-label/count-table Forge dead end. The stable action layer had not been tested for contextual functional differentiation in the current Forge history.
- branch: `null` — read-only source inspection plus synthetic reproduction only.

### Stable implementation inspected

`src/sparkbrain/v05/action.py` at stable main has an `AssemblyActionPolicy` whose learnable state is `scores[assembly_id][action]`, `visits[assembly_id]`, and one pending `(assembly_id, action)`. The chooser receives only `AssemblyActivation`; after maturity/suppression checks, the policy key is exactly `activation.assembly_id`. Exploration is deterministic round-robin for the first six visits and exploitation is greedy over the per-Assembly score table. Reward applies a scalar update only to the current pending Assembly/action cell.

Source blob: `792cba20ec5411633f12478d641adf35dba505e3`.

### Prototype / diagnostics

A source-faithful synthetic reproduction used one fixed Assembly `assembly-X` in alternating contexts A/B for 60 episodes. Correct action was `action-0` in A and `action-1` in B. Reward was 1 only for the context-correct action, 0 otherwise; learning rate 0.30 and six exploration visits matched stable defaults.

Comparator: the identical table policy was given an explicit ordinary context key by replacing the state key with `assembly-X|ctx=A/B`. This is intentionally a lookup/FSM reduction, not a proposed SparkBrain mechanism.

A second invariance diagnostic consistently renamed the three action labels (`action-0/action-1/withhold` -> `left/right/wait`) and renamed the reward targets with them for 30 episodes.

### Observations

- context-blind stable-key reproduction: total reward `29/60 = 0.4833`; after exploration it locks onto `action-0` and therefore succeeds on A but fails on B.
- final shared score table: `action-0=8.4`, `action-1=0.3`, `withhold=0.0` (floating-point representation aside).
- explicit context-key comparator: total reward `52/60 = 0.8667`; after each context finishes its own six-visit exploration schedule, it selects the correct action in both contexts.
- consistent action-label permutation produced an identical 30-episode reward sequence and isomorphic score table under renaming.

### Ordinary reduction

The behavior is fully explained by a tabular contextual-blindness reduction: function is attached to an external Assembly identifier and scalar reward table. With no context variable in the policy key, the same Assembly cannot represent incompatible context-conditioned action meanings; adding context to the key solves the toy task as an ordinary lookup/state-partition change. Action labels themselves carry no intrinsic learned semantics under consistent relabeling.

This does not show that upstream SparkBrain dynamics could never encode context by producing different Assembly identities. It only closes the narrower same-Assembly action-policy idea.

### Disposition

- status: `FORGE_DEAD_END`
- dead_end_reason: `The observed limitation and the successful comparator are both completely explained by ordinary tabular state-key privilege; no residual supports a distinct functional-meaning mechanism.`
- promotion_reason: `null`
- Utility request: `null`

## Metrics

Cumulative FAST_FORGE metrics since the R92 Forge role activation, reconciled from the prior latest surface:
- runs: `3`
- prototypes_attempted: `6` (two synthetic policy variants in this run)
- dead_ends: `5`
- interesting_observations_retained: `0`
- promotion_proposals: `0`
- later_admissions: `0`
- duplicate_or_rescue_rejects: `2`
- ownership_collisions: `0`
- ordinary_reduction_rejects: `5`

## Hard-floor confirmation

No PRE_FORMAL/FORMAL identity was created or consumed; no STARTED, official TEST/evidence/formal/sealed/freeze/preserve authority was created; no protected held-out/evaluator target was accessed; no consumed/immutable evidence was mutated; no response workflow was dispatched; no Forge branch was merged; no canonical candidate authority was claimed.
