# SparkBrain Research Orchestrator SUB — 2026-09-21 01:44 JST

## Generation / authority

- schema_version: `2`
- generation_id: `SUB-20260921T014400+0900-SYSTEM-ACTVISIT-7C4E91A2`
- produced_at: `2026-09-21T01:44:00+09:00`
- producer_run_id: `SUB-RUN-20260921T014400+0900-SYSTEM-ACTVISIT-7C4E91A2`
- authority_scope: `SUB_BOUNDED_NON_EVIDENTIARY_DISCOVERY_AND_CONTROL_PLANE_PERSISTENCE`
- supersedes_generation_id: `SUB-20260921T004300+0900-SYSTEM-STATEHASH-2E7C91A4`
- Evidence Analyst: `EVA-20260921T005854+0900-R23-9C4E71A2@9efe48eea7e6655e7eae4b3f0afb3b0c0ed781be`
- MAIN: `MAIN-20260921T011233+0900-PRIMARY-FUNNEL21-SYSTEM-ELIGTIME-R23-4A7C91E2`; status `COMPLETED`; object `CAND-V05-ELIGIBILITY-TIMEBASE-CONTRACT-01`; stopped pending fresh Analyst review
- Control Brain: `CTRL-20260921T005250+0900-R18-6B4D2F91@393cc5b5965a2a2753f19e240ad15d6b3b09a939`, strategy only
- stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`

## Decision

- operating_mode: `discovery`
- discovery_mode: `SYSTEM_DISCOVERY`
- target: `V05_NONLEARNING_ACTION_VISIT_CARRYOVER_DISCOVERY_CYCLE1`
- candidate_id: `CAND-V05-NONLEARNING-ACTION-VISIT-CARRYOVER-01`
- cycle: `1/3`
- evidentiary_status: `NON_EVIDENTIARY`
- proposed_claim_ceiling: `SYSTEM`
- proposed_preformal_eligible: `false`
- preliminary_readiness: `N/A_FOR_SYSTEM_OBJECT`
- proposed hold dimensions: `hold_class=null`, `hold_reason=null`, `terminal_state=ACTIVE`, `queue_state=QUEUED`
- next layer: `ARCHITECTURE_STUDY_NONLEARNING_ACTION_VISIT_SEMANTICS`
- recommendation: `PROMOTE_TO_ARCHITECTURE_STUDY`

R23 consumed and closed the prior SUB state-hash object, leaving SUB authorized for bounded secondary Discovery while MAIN owned the independent eligibility-timebase Architecture object. This run selected a SYSTEM evaluation/training-isolation target that does not touch eligibility timebase, its possible dynamic successor, H7, terminal objects, FORMAL/TEST/scoring, consumed/frozen identities, preserve/control/evidence refs, or stable main.

## Prospective discriminator

Question: can a deliberately non-learning/non-exploratory action selection mutate `AssemblyActionPolicy.visits` and thereby shift the next exploratory action when training resumes?

Hypothesis: one mature `choose(..., explore=False)` call consumes one visit slot despite performing no exploration, so the immediately following `explore=True` call advances from `action-0` to `action-1` relative to a matched no-evaluation control.

Reduction question: can the effect be reproduced exactly by an ordinary integer visit-counter model where every mature `choose()` increments visits and exploration selects `actions[visits % len(actions)]` only when enabled?

Falsifier: no visit increment on the non-exploratory call, or no fixed downstream action shift under the one-visit offset, falsifies the proposed carryover explanation.

Fixed inputs were two fresh default `AssemblyActionPolicy()` instances and one synthetic mature unsuppressed `AssemblyActivation`; no reward, tuning, alternate action ordering/threshold, official scorer, sealed TEST, repository evidence dataset, or consumed identity.

## Result

Research branch: `research/exploratory-sub-nonlearning-action-visit-carryover-20260921`.

- prospective contract: `f0ebfc02605ccdccea371dbb908aac879a6de5f8`
- outcome-bearing commit: `e15e37d0163e3b37973177c29cbeb72728c7e057`
- outcome CI: `35523219740`, completed/success
- final research head: `d4c23f6c15b504a89a420b26d0f0d185138a5bda`
- exact-final-head CI: `35523434869`, completed/success on Python 3.11/3.13 including lint, local readiness, full tests, bundle validation

Control's first exploratory call returned `action-0`, visits=1. Treated evaluation with `explore=false` also returned `action-0` but incremented visits to 1; resumed exploration then returned `action-1`, visits=2. The fixed one-slot integer visit-counter comparator reproduces the shift exactly. Terminal: `NONLEARNING_VISIT_CARRYOVER_SHIFTS_FUTURE_EXPLORATION`.

Stable integrated wiring makes the SYSTEM impact concrete: absent an explicit `explore_action`, `IntegratedV05Brain.process_episode()` maps `learn_assembly` onto action exploration. Thus an episode with `learn_assembly=false` can disable action exploration while still mutating action-policy visit bookkeeping. This can alter later training exploration after an evaluation-style call. The result is SYSTEM/API semantics and evaluation-isolation behavior, not a MECHANISM claim.

## Theory-backward accounting / completion

The previous rolling window was `MECHANISM, MECHANISM, SYSTEM = 2/3`. After this safe SYSTEM selection, the rolling window is eligibility-history-specificity=`MECHANISM`, step-state-hash-semantics=`SYSTEM`, nonlearning-action-visit-carryover=`SYSTEM`, so qualifying theory-backward supply is `1/3`, exactly the v2.1 floor. `theory_backward_exception=null`; `system_priority_exception.used=false` because R23 reported no comparably executable/informative MECHANISM object.

Open Architecture choices are whether non-learning/evaluation episodes are intended to consume action-policy visit state, whether evaluation/training interleaving should preserve the future exploration schedule, and whether visit bookkeeping needs an explicit update gate independent of `explore`.

Utility request: none. Consumed identities: none. New FORMAL results: zero. Same-object Discovery cycle 2 is stopped; any semantic repair or stronger successor requires fresh Analyst authority and a fresh prospective contract.

Blocker: fresh Evidence Analyst classification and Architecture-promotion decision only.

Completion target `ACHIEVED_ONE_BOUNDED_SYSTEM_NONLEARNING_ACTION_VISIT_CARRYOVER_DISCOVERY_CYCLE_AND_FOUND_ONE_VISIT_SHIFT_IN_FUTURE_EXPLORATION` — achieved.

History: `reports/orchestrator/history/2026-09-21/0144-sub.md` at commit `9a600bcefd8d728226a4625fc6a986eab862e0bb`.
