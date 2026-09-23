# FAST FORGE latest — same-Assembly action context is an ordinary table-key limitation

- schema_version: `2`
- generation_id: `FORGE-20260923T133600+0900-ACTION-CONTEXT-DEADEND-R92`
- produced_at: `2026-09-23T13:36:00+09:00`
- worker_role: `FAST_FORGE`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- overall_status: `FORGE_DEAD_END`

## Freshness / independence

Evidence Analyst remains R92 at `a05ab3f655a23eabd84c910ba337d64a948c168a`; stable main remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. MAIN candidate #34 is independently owned on `research/main-cand34-assembly-route-preformal-r92-cycle4`, observed at `43d0f25541a3c447d4c7156303647ae94f3119f4`. Recent Literature R36, Independent Audit R8, Methodology R81, Utility PF-R1 pointer-divergence state, and prior Forge history were re-read. No Relay branch was observed.

Forge avoided candidate #34, candidate #35, H7 FORMAL/provenance/preserve work, protected/consumed identities, and historical delayed-action/nonlearning-visit objects. Receptor-route aliasing and native responsibility/credit were rejected before execution as already-covered families.

No Forge branch was required; this run used read-only stable-source inspection and synthetic development probes only.

## Probe — can one Assembly learn context-dependent action meaning?

Stable `AssemblyActionPolicy` stores `scores[assembly_id][action]` and `visits[assembly_id]`; `choose()` receives an Assembly activation and keys the table only by `assembly_id`. It has deterministic six-visit round-robin exploration followed by greedy exploitation, and scalar reward updates only the pending Assembly/action cell.

Synthetic task: one fixed Assembly alternates contexts A/B for 60 episodes. A requires `action-0`; B requires `action-1`. With the stable context-blind key, total reward is `29/60 = 0.4833`, and after exploration the policy locks onto `action-0`, succeeding on A and failing on B.

Ordinary comparator: add context explicitly to the lookup key (`assembly-X|ctx=A/B`) while leaving the same table learner unchanged. That yields `52/60 = 0.8667`; after each context finishes its own exploration schedule, both contexts select their correct action. A consistent action-label rename also gives an identical reward sequence and isomorphic score table.

Disposition: `FORGE_DEAD_END`. This is fully reduced to ordinary tabular state-key privilege. The current action layer can attach reward value to Assembly/action cells, but the same Assembly cannot express incompatible context-conditioned action meanings unless context is represented upstream or explicitly added to the policy key. Adding the key is an ordinary lookup/FSM change, not evidence of a new mechanism. No promotion proposed.

## Boundaries / metrics

No Utility request. No branch mutation or merge. No PRE_FORMAL/FORMAL identity, STARTED, official scoring, protected held-out access, preserve/evidence mutation, or immutable-ref mutation occurred.

R92 FAST_FORGE cumulative metrics: runs `3`, prototypes `6`, dead ends `5`, retained interesting objects `0`, promotion proposals `0`, later admissions `0`, duplicate/rescue rejects `2`, ownership collisions `0`, ordinary-reduction rejects `5`.
