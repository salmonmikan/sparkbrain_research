# V05 Non-Learning Action Visit Carryover Discovery Contract

- candidate_id: `CAND-V05-NONLEARNING-ACTION-VISIT-CARRYOVER-01`
- discovery_mode: `SYSTEM_DISCOVERY`
- cycle: `1/3`
- evidentiary_status: `NON_EVIDENTIARY`
- claim_ceiling: `SYSTEM`
- preformal_eligible: `false`
- authoritative_source: stable `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- analyst_authority: `EVA-20260921T005854+0900-R23-9C4E71A2@9efe48eea7e6655e7eae4b3f0afb3b0c0ed781be`
- main_generation: `MAIN-20260921T011233+0900-PRIMARY-FUNNEL21-SYSTEM-ELIGTIME-R23-4A7C91E2`
- main_independence: does not touch `CAND-V05-ELIGIBILITY-TIMEBASE-CONTRACT-01`, its dynamic successor, eligibility decay, or any MAIN blocker/successor.

## Prospective question

Can a deliberately non-learning/non-exploratory action selection mutate `AssemblyActionPolicy.visits` and thereby shift the next exploratory action that would be selected when training resumes?

The integrated relevance is fixed prospectively from stable-main wiring: `IntegratedV05Brain.process_episode()` passes `explore=learn_assembly` when `explore_action` is omitted, while `AssemblyActionPolicy.choose()` increments `visits[assembly_id]` after every mature activation regardless of `explore`.

## Hypothesis

A single mature-Assembly evaluation call with `explore=False` increments the visit counter even though it performs no exploratory choice. Therefore the immediately following `explore=True` call will use the next exploration slot rather than the same slot a matched control would use without the evaluation call.

## Reduction question

Can any downstream action difference be reproduced exactly by an ordinary integer visit-counter model in which every `choose()` call increments `visits`, while exploration selects `actions[visits % len(actions)]` only when `explore=True` and `visits < exploration_visits`? If yes, the effect is a SYSTEM bookkeeping/evaluation-isolation property, not a MECHANISM candidate.

## Falsifier

The proposed carryover explanation is falsified if either:

1. `choose(mature_activation, explore=False)` leaves the visit counter unchanged; or
2. the next `explore=True` action is identical to the no-evaluation control despite the fixed one-visit offset under the first two exploration slots.

## Fixed input / procedure

- instantiate two fresh default `AssemblyActionPolicy()` objects: control and evaluation-treated;
- use one synthetic mature, unsuppressed `AssemblyActivation` with fixed `assembly_id="assembly-eval"`;
- control arm: call `choose(activation, explore=True)` once;
- treated arm: call `choose(activation, explore=False)` once, then call `choose(activation, explore=True)` once;
- record actions and visit counts after each call;
- fixed comparator predicts control training action `action-0`, treated evaluation action `action-0`, treated resumed-training action `action-1`, with visit counts `1` versus `2` after resumed training;
- no reward call, no parameter tuning, no alternate action ordering, no alternate visit threshold, no scorer, no sealed TEST, and no rescue cycle.

## Prospective terminal mapping

- evaluation increments visits and resumed training shifts exactly by one exploration slot -> `NONLEARNING_VISIT_CARRYOVER_SHIFTS_FUTURE_EXPLORATION`;
- evaluation increments visits but no fixed downstream shift -> `VISIT_MUTATION_WITHOUT_FIXED_EXPLORATION_SHIFT`;
- evaluation leaves visits unchanged -> `NONLEARNING_ACTION_STATE_INVARIANT`;
- any behavior not explained by the fixed integer visit-counter comparator -> `UNRESOLVED_ACTION_POLICY_STATE_EFFECT`.

## Promotion / stop mapping

This is a SYSTEM object only and is never PRE_FORMAL eligible. If the fixed carryover terminal occurs, recommend SYSTEM Architecture review because evaluation calls can alter later training exploration through action-policy bookkeeping; do not patch semantics in this object. If state is invariant, close/reject. Any API redesign separating evaluation visits from training visits requires a fresh object and fresh prospective contract.