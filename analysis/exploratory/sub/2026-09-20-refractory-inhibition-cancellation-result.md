# EXPLORATORY / NON_EVIDENTIARY — refractory inhibition cancellation result

- role: `SUB`
- mode: `discovery`
- exploratory_target: `REFRACTORY_INHIBITION_CANCELLATION_DISCOVERY_CYCLE1`
- candidate_pool_id: `NONE_SELF_SELECTED`
- exploration_cycle: `1/3`
- stable_main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- Evidence Analyst authority: `d6b14d826a0847e439dfedd86e363786d84e329a`
- prospective binding commit: `cfab761c4bb971593ddab3ab37cd0c8398d13b66`
- diagnostic commit after science-invariant lint fix: `c3b0b5d1de06ce38ff691ebf3e37183c1b2afbe3`
- diagnostic CI: `35467982649` — `completed/success`
- evidentiary_status: `NON_EVIDENTIARY`
- recommendation: `PROMOTE_TO_ARCHITECTURE_STUDY`

## Question

During the absolute refractory window, does a simultaneous positive arrival cancel an inhibitory arrival even though the field comment says positive drive is ignored during refractory, and can that difference survive to a fixed post-refractory probe?

## Inputs / implementation

The diagnostic used only a one-unit synthetic `TemporalExcitableField`, no connections, no receptors, and direct `SynapticArrival` injection. Initial potential was `0.5`, threshold `1.0`, refractory deadline `5.0 ms`. At `1.0 ms` the prospectively fixed arms were inhibition-only `-0.5`, paired same-time `-0.5/+0.5`, and excitation-only `+0.5`. At `5.1 ms` every arm received the same `+0.70` probe.

No repository dataset, checkpoint, formal raw, held-out/confirmatory TEST input, official scorer, consumed identity, MAIN result artifact, or immutable evidence was used. Production source was not modified.

The first CI on diagnostic commit `16a5d1ee4b890eefa6160ee6beef637b5332e275` stopped at Ruff lint before tests. The only fix was typing/direct attribute access; no current, time, threshold, comparator, or assertion was changed. CI `35467982649` then passed lint, local readiness, tests, and bundle validation on Python 3.11 and 3.13.

## Observation

At `1.0 ms`, passive decay moves the initial potential to approximately `0.472979734453`. The inhibition-only arm then reaches approximately `-0.027020265547`. The paired and excitation-only arms both remain at approximately `0.472979734453`: the paired `+0.5` cancels the simultaneous `-0.5` before the refractory clamp, while excitation-only is ignored by the clamp. No arm spikes during refractory.

At `5.1 ms`, after matched passive decay and the fixed `+0.70` probe, inhibition-only reaches approximately `0.678483730229` and does not spike. Paired and excitation-only reach approximately `1.076634328227` before reset and both spike once. Thus same-time positive current can erase the inhibitory membrane effect during refractory and alter a later post-refractory spike outcome.

The immediate mechanism is completely ordinary-reduced to existing `_deliver_group` control flow: aggregate positive and negative currents, compute `net_current = positive - negative`, then during refractory apply `potential += min(0.0, net_current)`. The effect requires no additional memory mechanism or scientific novelty claim.

## Falsification / reduction

This should reduce to `REJECT/ENGINEERING_NOTE_ONLY` if the supported field contract explicitly intends refractory current handling to operate on net current rather than independently ignore positive current, or if a fresh prospective architecture comparison shows no meaningful downstream difference under supported recurrent DEV contexts.

A promoted Architecture study should prospectively bind current `NET_THEN_REFRACTORY_CLAMP` against a read-only `IGNORE_POSITIVE_THEN_APPLY_INHIBITION` comparator with identical timestamps/currents and one fixed downstream observable. It must not rewrite v0.4 history, consumed evidence, or any formal result.

## Open choices / stop

Open semantic choices are whether absolute refractory means only spike prevention, positive-current rejection, or signed-current netting; whether inhibition must survive coincident excitation; and whether supported recurrent runtime conditions produce enough coincident mixed-sign arrivals for functional relevance.

Candidate next research layer: `ARCHITECTURE_STUDY_REFRACTORY_CURRENT_ACCOUNTING_SEMANTICS`.

SUB stops after this single bounded cycle. Evidence Analyst alone decides whether to promote, reduce, or reject it. Nothing in this exploratory result may be relabeled formal evidence.
