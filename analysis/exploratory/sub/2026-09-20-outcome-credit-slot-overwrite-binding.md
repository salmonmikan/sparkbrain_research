# EXPLORATORY / NON_EVIDENTIARY — outcome credit slot overwrite binding

- role: `SUB`
- mode: `discovery`
- candidate_pool_id: `NONE_SELF_SELECTED`
- exploratory_target: `OUTCOME_CREDIT_SLOT_OVERWRITE_DISCOVERY_CYCLE1`
- exploration_cycle: `1/3`
- stable_main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- analyst_authority: `eb1c305017d32c8c3efb0794e547b889e5a80461`
- evidentiary_status: `NON_EVIDENTIARY`

## Why independent of MAIN

MAIN owns `CAND-REFRACTORY-CURRENT-ACCOUNTING-01` and its complete Architecture critical path. This probe touches only v0.5 outcome-credit bookkeeping between `pending_activation`, `AssemblyActionPolicy.pending`, and `learn_outcome()`. It does not inspect or mutate MAIN's active refractory branch/object, Assembly follow-up, suppression detector work, Top-k, H7 construction, completed Temporal/topology-config objects, FORMAL/TEST/scoring/preserve/evidence surfaces, Utility control-plane work, or any consumed identity.

## Prospective question

Does `IntegratedV05Brain.learn_outcome()` bind a delayed outcome to the episode that produced it, or does any intervening episode overwrite the single pending activation/action slots so that prediction and reward credit are assigned to the most recently processed episode instead?

Current source exposes one mutable `pending_activation` slot on the brain and one mutable `pending` action slot on `AssemblyActionPolicy`; each new action/activation replaces the prior slot, while `learn_outcome()` accepts no episode or decision identity.

## Fixed synthetic diagnostic

Use only two synthetic mature `AssemblyActivation` objects, `assembly-A` and `assembly-B`, and the public v0.5 predictor/action/outcome interfaces. No repository dataset, world generator, trained checkpoint, held-out TEST input, formal scorer, or MAIN artifact is used.

Compare exactly two arms:
1. `IMMEDIATE_CONTROL`: make A the pending activation/action and immediately call `learn_outcome(next_event="event-A", reward=1.0)`.
2. `DEFERRED_AFTER_B`: make A pending, then make B pending before the same A-labelled outcome arrives, then call the same `learn_outcome(next_event="event-A", reward=1.0)` once.

Pre-bound observables:
- predictor count table key receiving `event-A`;
- action-score table key receiving the `+1.0` reward update;
- whether A remains uncredited in the deferred arm;
- whether the deferred arm exactly matches the currently pending B identity for both prediction and reward credit.

The diagnostic must not mutate production source or tune actions, rewards, activation maturity, or outcome label after observation.

## Reduction / falsification

Reduce to ordinary caller-order/API semantics and recommend `REJECT` if outcome attribution is explicitly guaranteed to be immediate-only by a supported contract, or if an intervening pending identity cannot redirect either predictor or action credit under the fixed diagnostic.

Recommend `PROMOTE_TO_ARCHITECTURE_STUDY` only if both prediction and action learning are reproducibly rebound from A to B by the intervening pending-state overwrite, because that would make asynchronous/delayed outcome handling an architecture-level temporal-credit contract rather than a single-component bookkeeping detail.

A future Architecture study, if authorized, must be freshly prospective and compare current single-slot attribution against an identity-bound read-only ledger/comparator under supported DEV caller order. It must not relabel this exploratory result as formal evidence.

Stop after this one bounded cycle for fresh Evidence Analyst review. Do not rescue/tune after outcome visibility.