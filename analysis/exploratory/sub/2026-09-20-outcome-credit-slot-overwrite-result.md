# EXPLORATORY / NON_EVIDENTIARY — outcome credit slot overwrite result

- role: `SUB`
- mode: `discovery`
- exploratory_target: `OUTCOME_CREDIT_SLOT_OVERWRITE_DISCOVERY_CYCLE1`
- candidate_pool_id: `NONE_SELF_SELECTED`
- exploration_cycle: `1/3`
- stable_main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- Evidence Analyst authority: `eb1c305017d32c8c3efb0794e547b889e5a80461`
- prospective binding commit: `b7f57b2c33b8650d1381b0d93e499abd2145e475`
- diagnostic commit: `d2ed668d06033bc702532f88a58ef0924568fddf`
- diagnostic CI: `35471075248` — Python 3.11/3.13 `completed/success`
- evidentiary_status: `NON_EVIDENTIARY`
- recommendation: `PROMOTE_TO_ARCHITECTURE_STUDY`

## Why independent of MAIN

MAIN owns `CAND-REFRACTORY-CURRENT-ACCOUNTING-01` and its complete Architecture critical path. This probe uses only v0.5 pending outcome-credit state and does not inspect, mutate, repair, or continue the Refractory object, its failed/pending workflow blocker, Assembly follow-up, suppression detector task, Top-k, H7, completed Temporal/topology-config work, FORMAL/TEST/scoring/preserve/evidence surfaces, Utility control-plane work, or any consumed identity.

## Question / reduction question

Does `IntegratedV05Brain.learn_outcome()` bind a delayed outcome to the episode/decision that produced it, or does an intervening decision overwrite the single pending activation/action slots and redirect prediction and reward credit to the latest identity?

If redirection occurs, is it fully explained by ordinary mutable single-slot bookkeeping rather than any additional learning mechanism?

## Inputs / implementation

The fixed diagnostic used only two synthetic mature `AssemblyActivation` objects (`assembly-A`, `assembly-B`) and public v0.5 predictor/action/outcome interfaces. It did not use repository datasets, world generators, checkpoints, formal raw, held-out/confirmatory TEST inputs, official scorers, consumed identities, or MAIN result artifacts. Production source was not modified.

`IMMEDIATE_CONTROL` sets A as the pending activation/action and immediately calls `learn_outcome(next_event="event-A", reward=1.0)`.

`DEFERRED_AFTER_B` sets A pending, then sets B pending before the same A-labelled outcome arrives, and calls `learn_outcome(next_event="event-A", reward=1.0)` once.

The diagnostic commit passed ordinary CI `35471075248`: Python 3.11 and 3.13 both passed lint, local readiness, full tests, and bundle validation.

## Observations

Immediate control credits prediction and reward to A: predictor state is `{"assembly-A": {"event-A": 1}}`, and `assembly-A/action-0` receives the fixed `+0.30` score update from reward `1.0` at learning rate `0.30`.

After B overwrites pending state, the exact same A-labelled outcome is instead credited to B: predictor state is `{"assembly-B": {"event-A": 1}}`; A is absent from predictor counts; A's action score remains `0.0`; and `assembly-B/action-0` receives the `+0.30` reward update.

The observation is exactly reduced to current source semantics. `IntegratedV05Brain` has one mutable `pending_activation`; `AssemblyActionPolicy` has one mutable `pending` action tuple; each newer decision overwrites the prior value; and `learn_outcome()` accepts no episode/decision identity. Therefore both prediction and reward learning use whichever identity is pending at call time.

Repository callsites found in evaluation/demo/tests currently invoke `learn_outcome()` immediately after each processed episode, so this Discovery does **not** establish prevalence or a bug in the currently exercised synchronous evaluation path. It characterizes what happens if the public API is used with delayed/asynchronous outcomes.

## Falsification / reduction

Reduce to `REJECT/ENGINEERING_NOTE_ONLY` if the supported contract explicitly guarantees immediate `process_episode -> learn_outcome` ordering and delayed/asynchronous outcome attribution is out of scope, or if a fresh supported DEV caller audit shows no legitimate path where another decision can intervene before its outcome.

The finding would also reduce if a prospectively defined identity-bound comparator shows no downstream learning difference under supported delayed caller order.

## Candidate next research layer / open choices

Candidate next layer: `ARCHITECTURE_STUDY_OUTCOME_ATTRIBUTION_SEMANTICS`.

Scientific/API choices still open:
- whether `learn_outcome()` is intentionally immediate-only or is expected to tolerate delayed outcomes;
- whether prediction and action reward should be bound to an episode/decision token rather than one mutable latest slot;
- whether supported DEV/integration callers can interleave a new episode before the prior outcome;
- whether any identity-bound ledger/comparator changes downstream prediction/action behavior under a prospectively fixed delayed-outcome schedule.

Recommendation to Evidence Analyst: `PROMOTE_TO_ARCHITECTURE_STUDY`, strictly as an API/temporal-credit attribution semantics question. This result remains `NON_EVIDENTIARY`, is not evidence for novelty or mechanistic distinctness, and cannot be relabeled formal.

SUB stops after this one bounded cycle. No cycle 2, production patch, formalization, or result-dependent tuning is authorized without fresh Evidence Analyst repartition.