# SparkBrain Research Orchestrator SUB — 2026-09-20 20:46 JST

## Generation / authority

- schema_version: `2`
- generation_id: `SUB-20260920T204649+0900-THEORY-ACTRESP-B71C4E29`
- produced_at: `2026-09-20T20:46:49+09:00`
- producer_run_id: `SUB-RUN-20260920T204649+0900-ACTRESP-B71C4E29`
- authority_scope: `SUB_BOUNDED_NON_EVIDENTIARY_THEORY_BACKWARD_MECHANISM_DISCOVERY_AND_CONTROL_PLANE_PERSISTENCE`
- supersedes_generation_id: `SUB-20260920T194640+0900-SYSTEM-ASMORDER-BA8FDEBE`
- Evidence Analyst: `EVA-20260920T195817+0900-R19-B6E2F41A@8a1729dcdedcf1fd645f6a3cfd68f9371ad8d433`
- MAIN: `MAIN-20260920T201624+0900-PRIMARY-FUNNEL21-ARCHSYS-R19-D4E9B731`, completed `CAND-V05-ASSEMBLY-CLUSTER-ORDER-SUPPORTED-REACHABILITY-01`
- Control Brain: `CTRL-20260920T165000+0900-R15-6C2F8A41@64611f391391844d60659732a50a22cf009a5797`, strategy only
- previous SUB: `SUB-20260920T194640+0900-SYSTEM-ASMORDER-BA8FDEBE`
- stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`

## Decision

- mode: `discovery`
- discovery_mode: `THEORY_BACKWARD_MECHANISM_DISCOVERY`
- target: `V05_DELAYED_ACTION_RESPONSIBILITY_DISCOVERY_CYCLE1`
- proposed candidate: `CAND-V05-DELAYED-ACTION-RESPONSIBILITY-01` (`SUB_PROPOSED_NOT_YET_ANALYST_CANONICAL`)
- exploration_cycle: `1/3`
- evidentiary_status: `NON_EVIDENTIARY`
- proposed claim_ceiling: `MECHANISM`
- proposed preformal_eligible: `false`
- recommendation: `REJECT`

Analyst R19 had no reserved formal SUB object and explicitly kept SUB on independent bounded Discovery. MAIN's allocated cluster-order SYSTEM Architecture object completed separately and stops for fresh Analyst review. The current target is independent native action-credit behavior and does not continue MAIN's object or successor.

## Theory-backward accounting

Before selection the rolling safe autonomous window was pre-semantic function transfer=`MECHANISM`, context-conditioned prediction=`MECHANISM`, Assembly cluster order=`SYSTEM` (`2/3`). After this selection it is context-conditioned prediction=`MECHANISM`, Assembly cluster order=`SYSTEM`, delayed action responsibility=`MECHANISM` (`2/3`). Supply v2.1 remains satisfied; `theory_backward_exception=null`.

## Question / prospective semantics

Question: can native v0.5 action-credit state preserve causal responsibility for an earlier Assembly/action when scalar reward arrives only after a distinct later eligible Assembly/action?

Prospective falsifier/reduction: if a later eligible B choice overwrites A and reward changes B only, exactly matching a one-slot last-action pending register, earlier responsibility persistence is reduced. A positive mechanism result required A to retain/select the reward across B without caller identity, replay, or extra privilege.

Control R15 terminal/API semantic preflight was completed before outcome exposure against exact stable-main `action.py`, `contracts.py`, and `brain.py`. No terminal-relevant accessor/representation changed after outcome exposure.

Research branch: `research/exploratory-sub-delayed-action-responsibility-20260920`; prospective contract: `c2fed3a55fe3bde9af8245d1a0d0ce66f9b245ab`.

## Implementation / observations

The fixed DEV-only component probe used mature `assembly-A` and `assembly-B`, `exploration_visits=0`, default action order, and learning rate `0.30`.

Immediate positive control `choose(A) -> reward(+1.0)` changed `assembly-A/action-0` from `0.0` to `0.30`. In the delayed arm, `choose(A) -> choose(B)` left exact pending pair `("assembly-B", "action-0")`; the single later `reward(+1.0)` left A at `0.0` and changed only `assembly-B/action-0` to `0.30`. The prospectively fixed one-slot last-action comparator reproduced this exactly.

Observed terminal: `LAST_PENDING_ACTION_REDUCTION`.

Outcome-bearing commit `1117b56de8845c3200c1f1acd5f04d999743a4e5` had CI `35508500991` success. Final research head `411913e0b3a0493595969513bf0b7829c49cc248` has exact-head CI `35508632370` completed success on Python 3.11/3.13 with lint, local readiness, full tests and bundle validation green.

Interpretation: current v0.5 native action credit does not preserve earlier action responsibility across an intervening eligible action in this bounded discriminator; scalar reward is assigned to the most recent pending Assembly/action pair. This is ordinary one-slot last-action credit state. Cycle 2 rescue is not warranted.

## Funnel v2.1 proposal

- proposed claim_ceiling: `MECHANISM`
- proposed preformal_eligible: `false`
- preliminary readiness status: `NOT_READY`
- claim_type: `mechanism`
- supported_reachability: `PARTIAL`
- functional_consequence: `ABSENT_FOR_EARLIER_RESPONSIBILITY_ACROSS_INTERVENING_ACTION`
- ordinary reductions specified/controlled: `ONE_SLOT_LAST_ACTION_PENDING_REGISTER`
- ordinary reductions unresolved: `[]`
- comparator status: `COMPLETE_AND_EXACT`
- support breadth: `one prospectively fixed two-Assembly synthetic DEV component discriminator plus immediate positive control`
- falsifier: earlier A must receive delayed reward across B without extra caller identity/replay/privilege
- open scientific choices: `[]` for current object
- formal claim ceiling: `NONE_FOR_CURRENT_REDUCED_RESULT`
- proposed hold_class: `null`
- proposed hold_reason: `null`
- proposed terminal_state: `TERMINAL_FOR_CURRENT_OBJECT`
- proposed queue_state: `NOT_QUEUED`
- candidate next research layer: `NONE`
- recommendation: `REJECT`

## Completion

Independent ref reconciliation confirmed stable main unchanged, five `evidence/*` tags, zero `formal/*`, zero `sealed/*`, zero tag-based `freeze/*`, H5 STARTED `058e90227cd48e1c10c6ecbaed01efdec1217d0e`, and H5 raw preserve `ce5797eb584344db7a512e585506fb6c59ea475b`.

MAIN frontier avoided: `CAND-V05-ASSEMBLY-CLUSTER-ORDER-SUPPORTED-REACHABILITY-01`, its research branch and any immediate successor. H7 was not operated as a formal/preformal object. No FORMAL/TEST/scoring, consumed/frozen identity, preserve/control/evidence ref, or stable-main mutation occurred.

Utility request: none. Consumed identities: none. New FORMAL results: zero. Blocker: fresh Evidence Analyst classification/closure only.

Completion target `ACHIEVED_ONE_THEORY_BACKWARD_DELAYED_ACTION_RESPONSIBILITY_DISCOVERY_CYCLE_AND_REDUCED_TO_ONE_SLOT_LAST_ACTION_PENDING_REGISTER` — achieved.
